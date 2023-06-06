import os
import shutil
import random
import numpy as np
import pandas as pd
import pyvista as pv
from tqdm import tqdm
from typing import List, Tuple, Literal

from pv_utils import *

random.seed(42)

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

DATA_DIR = os.path.join(current_dir, "../../data/dataset")
GEOMETRY_DIR = "Geometry"
RESULTS_DIR = "Results"
IMAGES_DIR = "Images"
TRAIN_DIR = "Train"
TEST_DIR = "Test"

GEOMETRY_TRANSFORMATIONS = ["Raw", "Pressure"]

RAW_DIR = "Raw/"
PRESSURE_DIR = "Pressure/"

TRAIN_PERCENTAGE = 0.9
ROTATION_STEP = 30


def get_train_test_geometries(
    geometry_files_dir: str,
    train_percentage: float
) -> Tuple[List[str], List[str]]:
    """
    This function returns two lists of geometries for training and testing.

    Args:
        geometry_files_dir (str): The directory containing geometry files.
        train_percentage (float): The percentage of geometries to use for training.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists of geometries for training and testing.
    """

    all_geometries = os.listdir(geometry_files_dir)
    all_geometries = [filename[:-4] for filename in all_geometries]
    # all_geometries = all_geometries[150:]

    print(all_geometries)

    random.shuffle(all_geometries)
    train_size = round(len(all_geometries) * train_percentage)
    train_geometries, test_geometries = \
        all_geometries[:train_size], all_geometries[train_size:]

    """ --- Stratified ---
    real_geometries = list(
        filter(lambda x: "SYNTHETIC" not in x, all_geometries))
    synthetic_geometries = list(
        filter(lambda x: "SYNTHETIC" in x, all_geometries))

    random.shuffle(real_geometries)
    random.shuffle(synthetic_geometries)
    train_size_real = int(len(real_geometries) * train_percentage)
    train_size_synthetic = int(len(synthetic_geometries) * train_percentage)

    train_geometries = real_geometries[:train_size_real] + \
        synthetic_geometries[:train_size_synthetic]

    test_geometries = real_geometries[train_size_real:] + \
        synthetic_geometries[train_size_synthetic:]
    """

    return (train_geometries, test_geometries)


def get_clim(transformation) -> List[float]:
    """
    Returns the clim values for a given transformation.

    Parameters:
        transformation (str): The name of the transformation.

    Returns:
        List[float]: The clim values for the given transformation.
    """

    if transformation == "Pressure":
        return [0.0, 0.1]
    else:
        return [0.0, 0.0]


def get_ambient(transformation: str) -> float:
    """
    This function returns the ambient lighting based on the transformation type.

    Args:
        transformation (str): The type of transformation.

    Returns:
        float: The ambient lighting.
    """

    if transformation == "Raw":
        return 0.1
    else:
        return 0.3


def generate_images_from_geometries(
    geometries: List[str],
    mode: Literal["train", "test"],
    transformation: str
):
    """
    This function generates images from geometries.

    Parameters:
        geometries (List[str]): A list of geometry filenames.
        mode (Literal["train", "test"]): The mode of the images to generate.
        transformation (str): The transformation to apply to the images.

    Returns:
        None
    """

    for filename in geometries:
        inner_geometry_path = os.path.join(DATA_DIR, GEOMETRY_DIR, filename + ".obj")
        outer_geometry_path = os.path.join(DATA_DIR, GEOMETRY_DIR, filename + ".vtk")
        result_path = os.path.join(DATA_DIR, PRESSURE_DIR, filename + ".csv")

        inner_geometry = pv.read(inner_geometry_path)
        outer_geometry = pv.read(outer_geometry_path)

        cfd_results = pd.read_csv(result_path)
        if transformation == "Raw":
            pass
        else:
            outer_geometry.point_data[transformation] = cfd_results.filter(
                regex=f".*{transformation}.*")

        save_path = None
        if (mode == "train"):
            save_path = os.path.join(
                DATA_DIR, IMAGES_DIR, TRAIN_DIR, transformation, filename
            )
        else:
            save_path = os.path.join(
                DATA_DIR, IMAGES_DIR, TEST_DIR, transformation, filename
            )

        if mode == "train":
            generate_rotating_snapshots(
                inner_geometry=inner_geometry,
                outer_geometry=outer_geometry,
                rotation_step=ROTATION_STEP,
                rotation_axis="x",
                clim=get_clim(transformation),
                ambient=get_ambient(transformation),
                save_path=save_path
            )
            generate_rotating_snapshots(
                inner_geometry=inner_geometry,
                outer_geometry=outer_geometry,
                rotation_step=ROTATION_STEP,
                rotation_axis="y",
                clim=get_clim(transformation),
                ambient=get_ambient(transformation),
                save_path=save_path
            )

        generate_rotating_snapshots(
            inner_geometry=inner_geometry,
            outer_geometry=outer_geometry,
            rotation_step=ROTATION_STEP,
            rotation_axis="z",
            clim=get_clim(transformation),
            ambient=get_ambient(transformation),
            save_path=save_path
        )

        yield


def clean_dir(path: str):
    try:
        shutil.rmtree(path=path)
    except OSError:
        os.makedirs(path)


if __name__ == "__main__":
    train_geometries, test_geometries = get_train_test_geometries(
        geometry_files_dir=os.path.join(DATA_DIR, PRESSURE_DIR),
        train_percentage=TRAIN_PERCENTAGE
    )

    print(train_geometries)

    for transformation in GEOMETRY_TRANSFORMATIONS:
        clean_dir(os.path.join(DATA_DIR, IMAGES_DIR, TRAIN_DIR, transformation))
        clean_dir(os.path.join(DATA_DIR, IMAGES_DIR, TEST_DIR, transformation))

        train_generator = generate_images_from_geometries(
            geometries=train_geometries,
            mode="train",
            transformation=transformation
        )
        for _ in tqdm(range(len(train_geometries))):
            next(train_generator)

        test_generator = generate_images_from_geometries(
            geometries=test_geometries,
            mode="test",
            transformation=transformation
        )
        for _ in tqdm(range(len(test_geometries))):
            next(test_generator)
