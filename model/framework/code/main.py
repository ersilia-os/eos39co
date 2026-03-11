import os
import csv
import sys
import tempfile
import numpy as np

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

# unimol_tools creates a 'logs/' dir in os.getcwd() at import time,
# which fails in read-only Singularity environments (CWD='/' → tries to create '/logs').
# Redirect by temporarily chdir-ing to a writable temp dir.
_log_dir = tempfile.mkdtemp()
_orig_dir = os.getcwd()
os.chdir(_log_dir)
from unimol_tools import UniMolRepr
os.chdir(_orig_dir)

root = os.path.dirname(os.path.abspath(__file__))

with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)
    smiles_list = [r[0] for r in reader]

clf = UniMolRepr(data_type='molecule', remove_hs=False, use_gpu=False)
unimol_repr = clf.get_repr(smiles_list, return_atomic_reprs=False)

X = np.array(unimol_repr['cls_repr'])

header = ["dim_{0}".format(str(i).zfill(3)) for i in range(X.shape[1])]

input_len = len(smiles_list)
output_len = X.shape[0]
assert input_len == output_len

with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for i in range(X.shape[0]):
        writer.writerow(list(X[i,:]))
