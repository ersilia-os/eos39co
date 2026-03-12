import os
import csv
import sys
import tempfile
import numpy as np

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])


_tmp_dir = tempfile.mkdtemp()
os.environ['UNIMOL_WEIGHT_DIR'] = _tmp_dir
os.environ['HF_HOME'] = _tmp_dir

from unimol_tools import UniMolRepr
import unimol_tools.models.unimol as _unimol_module
_unimol_module.WEIGHT_DIR = _tmp_dir

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
