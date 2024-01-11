import tensorflow as tf 
import matplotlib.pyplot as plt

DATA_DIR = "/mnt/Andromeda/Datasets/TAVI/Classification/Test/"

dataset = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    labels='inferred',
    label_mode='int',
    class_names=None,
    color_mode='rgb',
    batch_size=32,
    image_size=(256, 256),
    shuffle=False,
    seed=None,
    validation_split=None,
    subset=None,
    interpolation='bilinear',
    follow_links=False,
    crop_to_aspect_ratio=False
)


for element in dataset:
    print(element[0][0].shape)
    plt.figure()
    plt.imshow(element[0][0])
    break