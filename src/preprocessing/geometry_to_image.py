import os
import random
import numpy as np
import pyvista as pv
from tqdm import tqdm
from typing import List, Tuple, Literal

from utils import *

random.seed(1)

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

# DATA_DIR = os.path.join(current_dir, "../../data/dataset")
DATA_DIR = "/mnt/Data/Datasets/TAVI/"
PATIENTS_DIR = "Patients"
IMAGES_DIR = "Images-new"
TRAIN_DIR = "Train"
TEST_DIR = "Test"

RAW_DIR = "Raw"
CURVATURE_DIR = "Curvature"
PRESSURE_DIR = "Pressure"
STRESS_DIR = "Stress"
TRAIN_PERCENTAGE = 0.8
GEOMETRY_TRANSFORMATIONS = ["Stress"]
PRESSURE_LIM = [0.0, 0.4]
STRESS_LIM = [0.0, 0.5]
CURVATURE_LIM = [0.0, 0.05]


def get_train_test_patients(
    patients_dir: str, train_percentage: float
) -> Tuple[List[str], List[str]]:
    all_patients = os.listdir(patients_dir)
    random.shuffle(all_patients)
    train_size = round(len(all_patients) * train_percentage)
    train_patients, test_patients = all_patients[:train_size], all_patients[train_size:]
    return (train_patients, test_patients)


def generate_images(
    patients: List[str], transformation: str, mode: Literal["train", "test"]
):
    for patient in patients:
        patient_path = os.path.join(DATA_DIR, PATIENTS_DIR, patient)
        sizes = os.listdir(patient_path)
        for size in sizes:
            files_path = os.path.join(patient_path, size)
            input_file = get_file_with_extension(files_path, ".inp")
            pressure_file = get_file_with_extension(files_path, "CONTACT.csv")
            stress_file = get_file_with_extension(files_path, "SPOS.csv")
            aorta_file = get_file_with_extension(files_path, "AORTA.inp.stl")
            stent_file = get_file_with_extension(files_path, "STENT.obj")

            aorta = pv.read(aorta_file)
            stent = pv.read(stent_file)

            point_data = None

            if transformation == "Curvature":
                point_data = np.concatenate([aorta.curvature(curv_type="gaussian"), np.zeros((stent.n_points))])
                aorta = stent + aorta

                # point_data = aorta.curvature(curv_type="gaussian")

            elif transformation == "Pressure":
                result = get_pressure_result(input_file, pressure_file)
                point_data = np.concatenate([result["Value"].to_numpy(), np.zeros((stent.n_points))])
                aorta = stent + aorta
                # point_data = result["Pressure"].to_numpy()

            elif transformation == "Stress":
                result = get_stress_result(input_file, stress_file)
                point_data = np.concatenate([result["Value"].to_numpy(), np.zeros((stent.n_points))])
                aorta = stent + aorta

            elif transformation == "Raw":
                aorta = stent + aorta

            try:
                aorta.point_data[transformation] = point_data
            except Exception as e:
                print(e)
                print(aorta_file)

            save_path = None
            filename = patient + "_" + size
            if mode == "train":
                save_path = os.path.join(
                    DATA_DIR, IMAGES_DIR, TRAIN_DIR, transformation, filename
                )
            else:
                save_path = os.path.join(
                    DATA_DIR, IMAGES_DIR, TEST_DIR, transformation, filename
                )

            clim = None
            if transformation == "Pressure":
                clim = PRESSURE_LIM
            elif transformation == "Stress":
                clim = STRESS_LIM
            else:
                clim = CURVATURE_LIM
            generate_rotating_snapshots(aorta, save_path, clim)

        yield


if __name__ == "__main__":
    patients_dir = os.path.join(DATA_DIR, PATIENTS_DIR)
    train_patients, test_patients = get_train_test_patients(
        patients_dir, TRAIN_PERCENTAGE
    )

    for transformation in GEOMETRY_TRANSFORMATIONS:
        clean_dir(os.path.join(DATA_DIR, IMAGES_DIR, TRAIN_DIR, transformation))
        clean_dir(os.path.join(DATA_DIR, IMAGES_DIR, TEST_DIR, transformation))
        train_generator = generate_images(train_patients, transformation, "train")
        for _ in tqdm(range(len(train_patients))):
            next(train_generator)

            break
        break

        test_generator = generate_images(test_patients, transformation, "test")
        for _ in tqdm(range(len(test_patients))):
            next(test_generator)
