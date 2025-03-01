import os
from PIL import Image
from tqdm import tqdm

from utils import *

DATA_DIR = "/mnt/Data/Datasets/TAVI/"
IMAGES_DIR = "Images-new"
PAIRED_DIR = "Paired-Images-Stress"
TRAIN_DIR = "Train"
TEST_DIR = "Test"
INPUT_DIR = "Raw"
PRESSURE_DIR = "Pressure"
STRESS_DIR = "Stress"


def create_pair(image1: str, image2: str, save_path: str):
    image1 = Image.open(image1)
    image2 = Image.open(image2)
    new_image = Image.new("RGB", (image1.width + image2.width, image1.height))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1.width, 0))
    new_image.save(save_path)


if __name__ == "__main__":
    images_dir = os.path.join(DATA_DIR, IMAGES_DIR)
    paired_images_dir = os.path.join(DATA_DIR, PAIRED_DIR)

    # Process train images
    train_dir = os.path.join(images_dir, TRAIN_DIR)
    train_INPUT_DIR = os.path.join(train_dir, INPUT_DIR)
    train_pressure_dir = os.path.join(train_dir, PRESSURE_DIR)
    train_stress_dir = os.path.join(train_dir, STRESS_DIR)
    train_pairs_dir = os.path.join(paired_images_dir, TRAIN_DIR)
    clean_dir(train_pairs_dir)

    curvature_images = os.listdir(train_INPUT_DIR)

    for image in tqdm(curvature_images):
        image_path = os.path.join(train_INPUT_DIR, image)
        pressure_image_path = os.path.join(train_pressure_dir, image)
        stress_image_path = os.path.join(train_stress_dir, image)

        save_path = os.path.join(train_pairs_dir, image)
        # create_pair(image_path, pressure_image_path, save_path)
        create_pair(image_path, stress_image_path, save_path)

    # Process test images
    test_dir = os.path.join(images_dir, TEST_DIR)
    test_INPUT_DIR = os.path.join(test_dir, INPUT_DIR)
    test_pressure_dir = os.path.join(test_dir, PRESSURE_DIR)
    test_stress_dir = os.path.join(test_dir, STRESS_DIR)
    test_pairs_dir = os.path.join(paired_images_dir, TEST_DIR)
    clean_dir(test_pairs_dir)

    curvature_images = os.listdir(test_INPUT_DIR)

    for image in tqdm(curvature_images):
        image_path = os.path.join(test_INPUT_DIR, image)
        pressure_image_path = os.path.join(test_pressure_dir, image)
        stress_image_path = os.path.join(test_stress_dir, image)

        save_path = os.path.join(test_pairs_dir, image)
        # create_pair(image_path, pressure_image_path, save_path)
        create_pair(image_path, stress_image_path, save_path)
