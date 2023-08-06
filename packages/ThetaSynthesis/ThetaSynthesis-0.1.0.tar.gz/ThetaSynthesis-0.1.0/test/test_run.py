from CGRtools import smiles
from ThetaSynthesis import RetroTree
from ThetaSynthesis.synthon import DoubleHeadedSynthon
from pickle import dump

target = smiles('O=[N+]([O-])c2oc(/C=N/N1C(=O)NC(=O)C1)cc2')
target.canonicalize()
target.clean2d()

tree = RetroTree(target, synthon_class=DoubleHeadedSynthon, size=10000, iterations=int(5e4))

with open('results.pkl', 'wb') as f:
    dump(list(tree), f)
