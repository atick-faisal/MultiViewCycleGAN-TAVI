import os
import cv2
import numpy as np
from tqdm import tqdm
from skimage.metrics import (
    mean_squared_error,
    structural_similarity,
)
from sklearn.metrics import (
    precision_score,
    recall_score,
    fbeta_score,
    matthews_corrcoef,
    jaccard_score,
)

import matplotlib.pyplot as plt
from PIL import Image

INTENSITY_THRESHOLD = 19
MASK_PATH = "/mnt/Andromeda/TAVI Results/cp_masks"


def calculate_evaluation_metrics(
    ground_truth_path: str,
    predicted_path: str,
    intensity_threshold: int
):
    """
    Calculate evaluation metrics for a pair of ground truth and predicted images.
    Args:
        ground_truth_path (str): Path to the ground truth image.
        predicted_path (str): Path to the predicted image.
        intensity_threshold (int): Intensity threshold for binary conversion.
    Returns:
        tuple: A tuple containing precision, recall, f2 score, mcc, jaccard index,
        mse, iou score, and ssim.
    """
    ground_truth = cv2.imread(ground_truth_path)
    predicted = cv2.imread(predicted_path)

    ground_truth_gray = cv2.cvtColor(ground_truth, cv2.COLOR_BGR2GRAY)
    predicted_gray = cv2.cvtColor(predicted, cv2.COLOR_BGR2GRAY)

    ground_truth = ground_truth[:, 512:]
    predicted = predicted[:, 512:]
    ground_truth_gray = ground_truth_gray[:, 512:]
    predicted_gray = predicted_gray[:, 512:]

    _, background = cv2.threshold(
        ground_truth_gray, 254, 1, cv2.THRESH_BINARY_INV)

    _, mask_ground_truth = cv2.threshold(
        ground_truth_gray, intensity_threshold, 1, cv2.THRESH_BINARY)
    _, mask_predicted = cv2.threshold(
        predicted_gray, intensity_threshold, 1, cv2.THRESH_BINARY)

    # mask_ground_truth = (mask_ground_truth * background)[:, :, None] * ground_truth
    # mask_predicted = (mask_predicted * background)[:, :, None] * predicted

    # mask_ground_truth = cv2.cvtColor(mask_ground_truth, cv2.COLOR_BGR2RGB)
    # mask_predicted = cv2.cvtColor(mask_predicted, cv2.COLOR_BGR2RGB)

    mask_ground_truth = mask_ground_truth.astype(np.bool_)
    ground_truth[~mask_ground_truth, :] = (255, 255, 255)
    ground_truth = cv2.cvtColor(ground_truth, cv2.COLOR_BGR2RGB)
    mask_predicted = mask_predicted.astype(np.bool_)
    predicted[~mask_predicted, :] = (255, 255, 255)
    predicted = cv2.cvtColor(predicted, cv2.COLOR_BGR2RGB)

    ground_truth_img = Image.fromarray(ground_truth)
    predicted_img = Image.fromarray(predicted)

    ground_truth_img.save(os.path.join(
        MASK_PATH, ground_truth_path.split("/")[-1]))
    predicted_img.save(os.path.join(MASK_PATH, predicted_path.split("/")[-1]))


def calculate_metrics(image_folder):
    for file in tqdm(os.listdir(image_folder)):

        if file.endswith("_real.png"):
            base_name = file.replace("_real.png", "")
            real_image_path = os.path.join(image_folder, file)
            fake_image_path = os.path.join(
                image_folder, base_name + "_fake.png")

            if os.path.exists(fake_image_path):
                calculate_evaluation_metrics(
                    real_image_path, fake_image_path, INTENSITY_THRESHOLD
                )


def main():
    image_folder = \
        "/mnt/Andromeda/pytorch-CycleGAN-and-pix2pix/results/cp007/test_300/images/"
    calculate_metrics(image_folder)


if __name__ == "__main__":
    main()
