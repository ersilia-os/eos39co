import os
import csv
import sys
import shutil
import tempfile
import numpy as np
from concurrent.futures import ThreadPoolExecutor, TimeoutError

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
_weight_file = 'mol_pre_all_h_220816.pt'
_weight_src = os.path.join(root, '..', '..', 'checkpoints', _weight_file)
shutil.copy2(_weight_src, os.path.join(_tmp_dir, _weight_file))

clf = UniMolRepr(data_type='molecule', remove_hs=False, use_gpu=False)

BATCH_SIZE = 100
BATCH_TIMEOUT = 1000
MOL_TIMEOUT = 10
N_DIMS = 512
nan_row = [''] * N_DIMS


def get_repr(smiles):
    result = clf.get_repr(smiles, return_atomic_reprs=False)
    return np.array(result['cls_repr'])


rows = []
for i in range(0, len(smiles_list), BATCH_SIZE):
    batch = smiles_list[i:i + BATCH_SIZE]
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(get_repr, batch)
        try:
            batch_repr = future.result(timeout=BATCH_TIMEOUT)
            rows.extend(batch_repr.tolist())
        except TimeoutError:
            for smi in batch:
                with ThreadPoolExecutor(max_workers=1) as ex:
                    f = ex.submit(get_repr, [smi])
                    try:
                        mol_repr = f.result(timeout=MOL_TIMEOUT)
                        rows.append(mol_repr[0].tolist())
                    except TimeoutError:
                        rows.append(nan_row)

X = np.array(rows)
assert len(smiles_list) == X.shape[0]

header = ["dim_{0}".format(str(i).zfill(3)) for i in range(X.shape[1])]

with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for row in X:
        writer.writerow(row.tolist())

shutil.rmtree(_tmp_dir, ignore_errors=True)
