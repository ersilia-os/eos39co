import os
import csv
import sys
import numpy as np
from unimol_tools import UniMolRepr

input_file = sys.argv[1]
output_file = sys.argv[2]

root = os.path.dirname(os.path.abspath(__file__))

with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)
    smiles_list = [r[0] for r in reader]

clf = UniMolRepr(data_type='molecule', remove_hs=False, use_gpu=False)
unimol_repr = clf.get_repr(smiles_list, return_atomic_reprs=False)

X = np.array(unimol_repr['cls_repr'])

header = ["feat-{0}".format(i) for i in range(X.shape[1])]

input_len = len(smiles_list)
output_len = X.shape[0]
assert input_len == output_len

with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(X.shape[0]):
        writer.writerow(list(X[i,:]))
