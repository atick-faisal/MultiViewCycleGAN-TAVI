import os
import shutil
from utils import clean_dir

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

DATA_DIR = os.path.join(current_dir, "../../data/dataset")
CLASS_DIR = "Classification"
IMAGES_DIR = "Images"
TRAIN_DIR = "Train"
TEST_DIR = "Test"
GOOD_DIR = "Good"
BAD_DIR = "BAD"
PRESSURE_DIR = "Pressure"

GOOD_CASES = [
    "PATIENT-1_26",
    "PATIENT-2_26",
    "PATIENT-3_29",
    "PATIENT-5_26",
    "PATIENT-6_26",
    "PATIENT-7_34",
    "PATIENT-8_29",
    "PATIENT-9_26",
    "PATIENT-10_34",
    "PATIENT-11_34",
    "PATIENT-12_29",
    "PATIENT-13_26",
    "PATIENT-14_29",
    "PATIENT-15_29",
]

test_path = os.path.join(DATA_DIR, IMAGES_DIR, TEST_DIR, PRESSURE_DIR)
test_images = os.listdir(test_path)
good_cases = [
    item for item in test_images if any(good_case in item for good_case in GOOD_CASES)
]
dest_dir = os.path.join(DATA_DIR, CLASS_DIR, TEST_DIR, GOOD_DIR)
clean_dir(dest_dir)

for case in good_cases:
    source_path = os.path.join(test_path, case)
    dest_path = os.path.join(dest_dir, case)
    shutil.copy(source_path, dest_path)

bad_cases = [item for item in test_images if item not in good_cases]

dest_dir = os.path.join(DATA_DIR, CLASS_DIR, TEST_DIR, BAD_DIR)
clean_dir(dest_dir)

for case in bad_cases:
    source_path = os.path.join(test_path, case)
    dest_path = os.path.join(dest_dir, case)
    shutil.copy(source_path, dest_path)

    
train_path = os.path.join(DATA_DIR, IMAGES_DIR, TRAIN_DIR, PRESSURE_DIR)
train_images = os.listdir(train_path)
good_cases = [
    item for item in train_images if any(good_case in item for good_case in GOOD_CASES)
]
dest_dir = os.path.join(DATA_DIR, CLASS_DIR, TRAIN_DIR, GOOD_DIR)
clean_dir(dest_dir)

for case in good_cases:
    source_path = os.path.join(train_path, case)
    dest_path = os.path.join(dest_dir, case)
    shutil.copy(source_path, dest_path)

bad_cases = [item for item in train_images if item not in good_cases]

dest_dir = os.path.join(DATA_DIR, CLASS_DIR, TRAIN_DIR, BAD_DIR)
clean_dir(dest_dir)

for case in bad_cases:
    source_path = os.path.join(train_path, case)
    dest_path = os.path.join(dest_dir, case)
    shutil.copy(source_path, dest_path)