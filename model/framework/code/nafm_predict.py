"""NaFM inference helper: SMILES -> 1024-d scaffold-aware embedding.

Loads the pretrained NaFM GIN encoder and returns the pooled graph
representation (global_mean_pool of the encoder's node embeddings) — the same
feature NaFM's own downstream tasks consume (FinetunedGNN), NOT the contrastive
projection head. Runs on CPU, offline.

NaFM uses a fixed 9-element atom vocabulary (C, N, O, F, P, S, Cl, Br, I).
Molecules containing any other element (or invalid SMILES) yield an all-NaN row
so the output stays aligned with the input, one row per molecule.
"""
import os
import sys

import numpy as np
import torch
from rdkit import Chem
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn.pool import global_mean_pool

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_HERE, "nafm_src")                       # vendored gnn/ package
_CKPT = os.path.join(_HERE, "..", "..", "checkpoints", "NaFM.ckpt")  # Lightning ckpt (eosvc)

EMB_DIM = 1024  # NaFM embedding dim (checkpoint emb_dim=1024)

# vendored NaFM code uses flat `gnn...` imports, so its dir must be on sys.path
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

# Featurization vocabularies (must match NaFM's inference.py exactly)
ATOM_LIST = [6, 7, 8, 9, 15, 16, 17, 35, 53]
CHIRALITY = [Chem.rdchem.ChiralType.CHI_UNSPECIFIED, Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW,
             Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW, Chem.rdchem.ChiralType.CHI_OTHER]
CHARGE = [-1, -2, 1, 2, 0]
BONDS = [Chem.rdchem.BondType.SINGLE, Chem.rdchem.BondType.DOUBLE,
         Chem.rdchem.BondType.TRIPLE, Chem.rdchem.BondType.AROMATIC]
BONDDIR = [Chem.rdchem.BondDir.NONE, Chem.rdchem.BondDir.ENDUPRIGHT, Chem.rdchem.BondDir.ENDDOWNRIGHT]

_encoder = None


def _load_encoder():
    """Load the pretrained NaFM GIN encoder (representation model) on CPU."""
    global _encoder
    if _encoder is None:
        from gnn.pre_module import LNNP

        torch.set_num_threads(max(1, os.cpu_count() or 1))
        lnnp = LNNP.load_from_checkpoint(_CKPT, map_location="cpu")
        lnnp.eval()
        # downstream feature = pooled representation_model output (pre-projection)
        _encoder = lnnp.model.pretrain_gnn.representation_model
        _encoder.eval()
    return _encoder


def _to_data(smi):
    """SMILES -> PyG Data, or None if invalid or contains an out-of-vocab atom."""
    if smi is None:
        return None
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return None
    if any(a.GetAtomicNum() not in ATOM_LIST for a in mol.GetAtoms()):
        return None  # NaFM's 9-element vocabulary does not cover this molecule
    x = torch.tensor(
        [[ATOM_LIST.index(a.GetAtomicNum()),
          CHIRALITY.index(a.GetChiralTag()) if a.GetChiralTag() in CHIRALITY else 3,
          CHARGE.index(a.GetFormalCharge()) if a.GetFormalCharge() in CHARGE else 4]
         for a in mol.GetAtoms()], dtype=torch.long)
    ei, ea = [], []
    for b in mol.GetBonds():
        bt, bd = b.GetBondType(), b.GetBondDir()
        if bt not in BONDS or bd not in BONDDIR:
            return None  # out-of-vocabulary bond type/direction -> NaN row
        s, e = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        feat = [BONDS.index(bt), BONDDIR.index(bd)]
        ei += [(s, e), (e, s)]; ea += [feat, feat]
    edge_index = torch.tensor(ei, dtype=torch.long).t().contiguous() if ei else torch.zeros((2, 0), dtype=torch.long)
    edge_attr = torch.tensor(ea, dtype=torch.long) if ea else torch.zeros((0, 2), dtype=torch.long)
    return Data(x=x, edge_index=edge_index, edge_attr=edge_attr, num_nodes=x.size(0))


def predict(smiles_list):
    """Return an (N, 1024) float32 array of NaFM embeddings; NaN rows for
    invalid SMILES or molecules outside the 9-element atom vocabulary."""
    enc = _load_encoder()
    valid_idx, datas = [], []
    for i, smi in enumerate(smiles_list):
        d = _to_data(smi)
        if d is not None:
            valid_idx.append(i)
            datas.append(d)

    out = np.full((len(smiles_list), EMB_DIM), np.nan, dtype=np.float32)
    if datas:
        loader = DataLoader(datas, batch_size=64, shuffle=False)
        rows = []
        with torch.no_grad():
            for batch in loader:
                rep = enc(batch)
                emb = global_mean_pool(rep, batch.batch)
                rows.append(emb.cpu().numpy().astype(np.float32))
        emb = np.concatenate(rows, axis=0)
        for row, i in enumerate(valid_idx):
            out[i] = emb[row]
    return out
