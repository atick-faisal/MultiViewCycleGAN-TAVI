import numpy as np
import pyvista as pv
from PIL import Image
from typing import List, Literal
from matplotlib.pyplot import cm
from pyvista.core.pointset import PolyData
from matplotlib.colors import ListedColormap


def generate_rotating_snapshots(
    geometry: PolyData,
    save_path: str,
    clim: List[float] = [0.0, 0.4],
    rotation_axis: Literal["x", "y", "z"] = "z",
    rotation_step: int = 30,
    ambient: float = 0.3,
) -> None:
    """
    Generates a series of rotating snapshots of a 3D geometry and saves them as images.

    Parameters:
    - geometry (PolyData): The 3D geometry to be visualized and rotated.
    - save_path (str): The path where the generated snapshots will be saved.
    - clim (List[float], optional): The color range for mapping scalar values to colors. Default is [0.0, 0.4].
    - rotation_axis (Literal["x", "y", "z"], optional): The axis around which the rotation will occur. Default is "z".
    - rotation_step (int, optional): The angle (in degrees) by which the geometry will be rotated at each step. Default is 30.
    - ambient (float, optional): The ambient lighting coefficient. Default is 0.3.

    Returns:
    - None

    """
    pl = pv.Plotter(off_screen=True)
    pl.enable_anti_aliasing()
    pl.set_background("white")

    # Required for correcting the geometry orientation
    geometry.rotate_x(90, inplace=True)

    jet = cm.get_cmap("jet", 16)
    cmap = jet(np.linspace(0, 1, 16))

    # ... Stress
    # cmap[0:5, 3] = 0.3

    # ... Pressure & Curvature
    cmap[0, 3] = 0.3

    pl.add_mesh(
        mesh=geometry,
        cmap=ListedColormap(cmap),
        show_scalar_bar=False,
        clim=clim,
        ambient=ambient,
        smooth_shading=True,
        lighting=True,
    )

    # This configuration works best to get a good snapshot
    pl.camera.zoom(2.0)
    pl.camera.focal_point = (0, 0, 20.0)
    pl.camera.elevation = -20

    # geometry.rotate_z(130, inplace=True)

    for i in range(360 // rotation_step):
        if rotation_axis == "x":
            geometry.rotate_x(rotation_step, inplace=True)
        elif rotation_axis == "y":
            geometry.rotate_y(rotation_step, inplace=True)
        elif rotation_axis == "z":
            geometry.rotate_z(rotation_step, inplace=True)
        else:
            raise ValueError("Rotation axis is not correct")

        pl.clear()
        pl.add_mesh(
            mesh=geometry,
            cmap=ListedColormap(cmap),
            show_scalar_bar=False,
            clim=clim,
            ambient=ambient,
            smooth_shading=True,
            lighting=True,
            opacity=1.0
        )
        pl.show(auto_close=False)
        image = Image.fromarray(pl.image[:, 128:-128, :])
        image.save(save_path + "_{:s}_{:03d}.png".format(rotation_axis, i))

    # pl.show()
    pl.close()
    pl.deep_clean()
