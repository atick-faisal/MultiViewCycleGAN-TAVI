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

INTENSITY_THRESHOLD = 40


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
    ground_truth = cv2.imread(ground_truth_path, cv2.IMREAD_GRAYSCALE)
    predicted = cv2.imread(predicted_path, cv2.IMREAD_GRAYSCALE)

    ground_truth = ground_truth[:, 512:]
    predicted = predicted[:, 512:]

    _, background = cv2.threshold(
        ground_truth, 254, 1, cv2.THRESH_BINARY_INV)

    _, mask_ground_truth = cv2.threshold(
        ground_truth, intensity_threshold, 1, cv2.THRESH_BINARY)
    _, mask_predicted = cv2.threshold(
        predicted, intensity_threshold, 1, cv2.THRESH_BINARY)

    mask_ground_truth = mask_ground_truth * background
    mask_predicted = mask_predicted * background

    intersection = np.logical_and(mask_ground_truth, mask_predicted)
    union = np.logical_or(mask_ground_truth, mask_predicted)
    iou_score = np.sum(intersection) / np.sum(union)

    mask_ground_truth_flat = mask_ground_truth.flatten()
    mask_predicted_flat = mask_predicted.flatten()

    ssim = structural_similarity(ground_truth, predicted)
    precision = precision_score(mask_ground_truth_flat, mask_predicted_flat)
    recall = recall_score(mask_ground_truth_flat, mask_predicted_flat)
    f2 = fbeta_score(mask_ground_truth_flat, mask_predicted_flat, beta=2)
    mcc = matthews_corrcoef(mask_ground_truth_flat, mask_predicted_flat)
    jaccard = jaccard_score(mask_ground_truth_flat, mask_predicted_flat)
    mse = mean_squared_error(ground_truth * background, predicted * background) \
        / np.max(ground_truth)

    return precision, recall, f2, mcc, jaccard, mse, iou_score, ssim


def calculate_metrics(image_folder):
    """
    Calculate evaluation metrics for a set of ground truth and predicted images.
    Args:
        image_folder (str): Path to the folder containing the images.
    Returns:    
        tuple: A tuple containing average mse, average iou, average ssim, average precision,
        average recall, average f2 score, average mcc, and average jaccard index.
    """

    mse_values = []
    iou_values = []
    ssim_values = []
    precision_values = []
    recall_values = []
    f2_values = []
    mcc_values = []
    jaccard_values = []

    for file in tqdm(os.listdir(image_folder)):

        if file.endswith("_real.png"):
            base_name = file.replace("_real.png", "")
            real_image_path = os.path.join(image_folder, file)
            fake_image_path = os.path.join(
                image_folder, base_name + "_fake.png")

            if os.path.exists(fake_image_path):
                precision, recall, f2, mcc, jaccard, \
                    mse, iou, ssim = calculate_evaluation_metrics(
                        real_image_path, fake_image_path, INTENSITY_THRESHOLD
                    )

                precision_values.append(precision)
                recall_values.append(recall)
                f2_values.append(f2)
                mcc_values.append(mcc)
                jaccard_values.append(jaccard)
                mse_values.append(mse)
                iou_values.append(iou)
                ssim_values.append(ssim)

    avg_mse = np.mean(mse_values)
    avg_iou = np.mean(iou_values)
    avg_ssim = np.mean(ssim_values)
    avg_precision = np.mean(precision_values)
    avg_recall = np.mean(recall_values)
    avg_f2 = np.mean(f2_values)
    avg_mcc = np.mean(mcc_values)
    avg_jaccard = np.mean(jaccard_values)

    return avg_mse, avg_iou, avg_ssim, avg_precision, \
        avg_recall, avg_f2, avg_mcc, avg_jaccard


def main():
    image_folder = \
        "/mnt/Andromeda/pytorch-CycleGAN-and-pix2pix/results/cp007/test_300/images/"
    avg_mse, avg_iou, avg_ssim, avg_precision, avg_recall, \
        avg_f2, avg_mcc, avg_jaccard = calculate_metrics(image_folder)

    print(f"Average MSE: {avg_mse}")
    print(f"Average IOU: {avg_iou}")
    print(f"Average SSIM: {avg_ssim}")
    print(f"Average Precision: {avg_precision}")
    print(f"Average Recall: {avg_recall}")
    print(f"Average F2: {avg_f2}")
    print(f"Average MCC: {avg_mcc}")
    print(f"Average Jaccard: {avg_jaccard}")


if __name__ == "__main__":
    main()
