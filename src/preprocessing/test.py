import os
import shutil
import random
import meshio
import numpy as np
import pandas as pd
import pyvista as pv
from tqdm import tqdm
from typing import List, Tuple, Literal

from pv_utils import *
from abaqus_utils import *

random.seed(42)

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

DATA_DIR = os.path.join(current_dir, "../../data/dataset")
PATIENTS_DIR = "Patients"
IMAGES_DIR = "Images"
TRAIN_DIR = "Train"
TEST_DIR = "Test"

RAW_DIR = "Raw"
CURVATURE_DIR = "Curvature"
PRESSURE_DIR = "Pressure"

GEOMETRY_TRANSFORMATIONS = ["Raw", "Curvature", "Pressure"]

TRAIN_PERCENTAGE = 0.9
ROTATION_STEP = 30

patients_path = os.path.join(DATA_DIR, PATIENTS_DIR)
patients = os.listdir(patients_path)

for patient in patients:
    sizes_path = os.path.join(patients_path, patient)
    sizes = os.listdir(sizes_path)
    for size in sizes:
        files_path = os.path.join(sizes_path, size)
        files = os.listdir(files_path)
        input_file = [fi for fi in files if fi.endswith(".inp")][0]
        result_file = [fi for fi in files if fi.endswith(".csv")][0]
        try:
            result = get_ordered_result(
                inp_file_path=os.path.join(files_path, input_file),
                result_path=os.path.join(files_path, result_file),
            )
        except:
            print(os.path.join(files_path, input_file))
        aorta_obj = [fi for fi in files if fi.endswith("AORTA.obj")][0]
        stent_obj = [fi for fi in files if fi.endswith("STENT.obj")][0]
        mesh = meshio.read(os.path.join(files_path, input_file))
        mesh.write(os.path.join(files_path, input_file + ".vtk"))
        mesh.write(os.path.join(files_path, input_file + ".stl"))
        aorta = pv.read(os.path.join(files_path, input_file + ".vtk"))
        aorta_obj = pv.read(os.path.join(files_path, input_file + ".stl"))
        stent_obj = pv.read(os.path.join(files_path, stent_obj))
        curvature = aorta_obj.curvature(curv_type="gaussian")
        aorta_obj.point_data["C"] = curvature
        # aorta.rotate_x(100, inplace=True)
        # aorta.rotate_y(-10, inplace=True)
        # aorta.rotate_z(90, inplace=True)

        print(aorta.center)
        # aorta.translate([3.5534105499999997, -31.2767539, 16.10928725], inplace=True)
        print(aorta.center)
        # aorta_obj.plot()

        # aorta_obj.rotate_x(110, inplace=True)
        # aorta.rotate_y(-10, inplace=True)
        # aorta.rotate_z(270, inplace=True)

        # pl = pv.Plotter()
        # pl.enable_anti_aliasing()
        # # pl.set_background("white")
        # # pl.camera_position = "xy"
        
        # pl.add_mesh(aorta_obj)
        # pl.camera.zoom(2.0)
        # pl.camera.focal_point = (0, 0, 20.0)
        # pl.show()
        # pl.close()


        save_path = os.path.join(
            DATA_DIR, 
            IMAGES_DIR, 
            TRAIN_DIR,
            CURVATURE_DIR, 
            input_file[:-4]
        )
        generate_rotating_snapshots(
            inner_geometry=stent_obj,
            outer_geometry=aorta_obj,
            rotation_step=30,
            rotation_axis="z",
            clim=[0, 0.05],
            ambient=0.3,
            save_path=save_path
        )

    #     break
    # break
