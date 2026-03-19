import os
import csv
import sys
import shutil
import tempfile
import numpy as np

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])

# unimol_tools writes weights, HF cache and logs to locations that are
# read-only inside Apptainer (site-packages, cwd=/). Redirect everything
# to a fresh writable temp directory for this run.
_tmp_dir = tempfile.mkdtemp()
os.environ['UNIMOL_WEIGHT_DIR'] = _tmp_dir
os.environ['HF_HOME'] = _tmp_dir

_orig_dir = os.getcwd()
os.chdir(_tmp_dir)  # base_logger creates ./logs relative to cwd at import time
from unimol_tools import UniMolRepr
# Patch WEIGHT_DIR in every unimol_tools submodule that defines it, not just
# unimol_tools.models.unimol — conformer.py and others keep their own copy.
for _m in list(sys.modules.values()):
    if 'unimol_tools' in getattr(_m, '__name__', '') and hasattr(_m, 'WEIGHT_DIR'):
        _m.WEIGHT_DIR = _tmp_dir
os.chdir(_orig_dir)

with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)
    smiles_list = [r[0] for r in reader]

root = os.path.dirname(os.path.abspath(__file__))
_checkpoints_dir = os.path.join(root, '..', '..', 'checkpoints')
_weight_file = 'mol_pre_all_h_220816.pt'
_weight_src = os.path.join(_checkpoints_dir, _weight_file)
if os.path.isfile(_weight_src):
    shutil.copy2(_weight_src, os.path.join(_tmp_dir, _weight_file))

clf = UniMolRepr(data_type='molecule', remove_hs=False, use_gpu=False)
unimol_repr = clf.get_repr(smiles_list, return_atomic_reprs=False)

X = np.array(unimol_repr['cls_repr'])

assert len(smiles_list) == X.shape[0]

header = ["dim_{0}".format(str(i).zfill(3)) for i in range(X.shape[1])]

with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for row in X:
        writer.writerow(row.tolist())

shutil.rmtree(_tmp_dir, ignore_errors=True)
