import cv2
import numpy as np
import os
import math
from skimage.metrics import structural_similarity as ssim

def calculate_metrics(image_folder):
    mse_values = []
    rmse_values = []
    ssim_values = []

    for file in os.listdir(image_folder):
        
        if file.endswith("_target.png"):
            base_name = file.replace("_target.png", "")
            real_image_path = os.path.join(image_folder, file)
            fake_image_path = os.path.join(image_folder, base_name + "_fake.png")

            if os.path.exists(fake_image_path):
                real_image = cv2.imread(real_image_path)
                fake_image = cv2.imread(fake_image_path)
                real_image = cv2.resize(real_image, (256, 256))

                # Ensure the images are the same size
                if real_image.shape == fake_image.shape:
                    mse = np.mean((real_image - fake_image) ** 2)
                    rmse = math.sqrt(mse)
                    # ssim_value = ssim(real_image, fake_image)

                    mse_values.append(mse)
                    rmse_values.append(rmse)
                    # ssim_values.append(ssim_value)

    avg_mse = np.mean(mse_values)
    avg_rmse = np.mean(rmse_values)
    # avg_ssim = np.mean(ssim_values)

    return avg_mse, avg_rmse, 0

# Usage
image_folder = '/home/ai/Downloads/cyclegan_256/'
avg_mse, avg_rmse, avg_ssim = calculate_metrics(image_folder)
print(f"Average MSE: {avg_mse}, Average RMSE: {avg_rmse}, Average SSIM: {avg_ssim}")



# Usage
# image_folder = "/home/ai/Downloads/Nov-19-07-05AM"
# avg_mse, avg_rmse = calculate_mse_rmse(image_folder)
# print(f"Average MSE: {avg_mse}, Average RMSE: {avg_rmse}")

# CycleGAN
# Average MSE: 16.839275723411923, Average RMSE: 4.097746027980363, Average SSIM: 0.8962748288778994
# Average MSE: 14.03707988678463, Average RMSE: 3.7412332685817997, Average SSIM: 0

# UNet
# Average MSE: 13.77025690532866, Average RMSE: 3.6943809085779313, Average SSIM: 0.9308193108223433
# Average MSE: 12.31149028596424, Average RMSE: 3.492069471009254

