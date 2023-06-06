import os
from abaqus_utils import *

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

DATA_DIR = os.path.join(current_dir, "../../data/dataset")

inp_file_path = os.path.join(DATA_DIR, "AORTA_FULL.inp")
result_path = os.path.join(DATA_DIR, "AORTA_FULL.csv")

ordered_result = get_ordered_result(inp_file_path, result_path)
ordered_result.to_csv(os.path.join(DATA_DIR, "merged.csv"), index=False)
