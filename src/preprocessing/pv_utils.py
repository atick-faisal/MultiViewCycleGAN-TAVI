import numpy as np
import pyvista as pv
from PIL import Image
from typing import List, Literal
from matplotlib.pyplot import cm
from pyvista.core.pointset import PolyData
from matplotlib.colors import ListedColormap

jet = cm.get_cmap("jet", 64)
cmap = jet(np.linspace(0, 1, 64))
# cmap[0, 3] = 0.7


def generate_rotating_snapshots(
    inner_geometry: PolyData,
    outer_geometry: PolyData,
    rotation_step: int,
    rotation_axis: Literal["x", "y", "z"],
    clim: List[float],
    ambient: float,
    save_path: str
):
    """
    Generate rotating snapshots of a 3D geometry.

    Parameters
    ----------
    geometry : vtk.vtkPolyData
        The input geometry to be visualized.
    rotation_step : int
        The rotation step in degrees.
    rotation_axis : {'x', 'y', 'z'}
        The axis of rotation.
    clim : list of float
        The color range limits.
    ambient : float
        The ambient lighting amount
    save_path : str
        The path to save the images.

    Returns
    -------
    None

    """

    pl = pv.Plotter(off_screen=True)
    pl.enable_anti_aliasing()
    pl.set_background("white")

    inner_geometry.rotate_x(90, inplace=True)
    outer_geometry.rotate_x(90, inplace=True)

    pl.add_mesh(
        mesh=inner_geometry,
        cmap=cm.jet,
        show_scalar_bar=False,
        clim=clim,
        ambient=ambient,
        smooth_shading=True,
        lighting=True,
        opacity=0.5
    )

    pl.add_mesh(
        mesh=outer_geometry,
        cmap=ListedColormap(cmap),
        show_scalar_bar=False,
        clim=clim,
        ambient=ambient,
        smooth_shading=True,
        lighting=True
    )

    pl.camera.zoom(2.0)

    pl.camera.focal_point = (0, 0, 20.0)
    pl.camera.elevation = -20
    
    

    for i in range(360 // rotation_step):
        if rotation_axis == "x":
            inner_geometry.rotate_x(rotation_step, inplace=True)
            outer_geometry.rotate_x(rotation_step, inplace=True)
        elif rotation_axis == "y":
            inner_geometry.rotate_y(rotation_step, inplace=True)
            outer_geometry.rotate_y(rotation_step, inplace=True)

        elif rotation_axis == "z":
            inner_geometry.rotate_z(rotation_step, inplace=True)
            outer_geometry.rotate_z(rotation_step, inplace=True)
            pl.clear()
            pl.add_mesh(
                mesh=inner_geometry,
                cmap=cm.jet,
                show_scalar_bar=False,
                clim=clim,
                ambient=ambient,
                smooth_shading=True,
                lighting=True,
                opacity=0.1
            )

            pl.add_mesh(
                mesh=outer_geometry,
                cmap=ListedColormap(cmap),
                show_scalar_bar=False,
                clim=clim,
                ambient=ambient,
                smooth_shading=True,
                lighting=True
            )
        else:
            raise ValueError("Roatation axis is not correct")

        pl.show(auto_close=False)
        image = Image.fromarray(pl.image[:, 128:-128, :])
        image.save(save_path + "_{:s}_{:03d}.png".format(rotation_axis, i))

    pl.close()
    pl.deep_clean()


def generate_rotating_snapshots_for_target(
    geometry: PolyData,
    rotation_step: int,
    rotation_axis: Literal["x", "y", "z"],
    clim: List[float],
    ambient: float,
    save_path: str
):
    """
    Generate rotating snapshots of a 3D geometry.

    Parameters
    ----------
    geometry : vtk.vtkPolyData
        The input geometry to be visualized.
    rotation_step : int
        The rotation step in degrees.
    rotation_axis : {'x', 'y', 'z'}
        The axis of rotation.
    clim : list of float
        The color range limits.
    ambient : float
        The ambient lighting amount
    save_path : str
        The path to save the images.

    Returns
    -------
    None

    """

    pl = pv.Plotter(off_screen=True)
    pl.enable_anti_aliasing()
    pl.set_background("white")
    
    # geometry.translate([3.5534105499999997, -31.2767539, 16.10928725], inplace=True)
    geometry.rotate_x(90, inplace=True)

    pl.add_mesh(
        mesh=geometry,
        cmap=cm.jet,
        show_scalar_bar=False,
        clim=clim,
        ambient=ambient,
        smooth_shading=True,
        lighting=True
    )

    pl.camera.zoom(2.0)

    pl.camera.focal_point = (0, 0, 20.0)
    pl.camera.elevation = -20

    
    for i in range(360 // rotation_step):
        if rotation_axis == "x":
            geometry.rotate_x(rotation_step, inplace=True)
        elif rotation_axis == "y":
            geometry.rotate_y(rotation_step, inplace=True)
            
        elif rotation_axis == "z":
            geometry.rotate_z(rotation_step, inplace=True)
            pl.clear()
            pl.add_mesh(
                mesh=geometry,
                cmap=ListedColormap(cmap),
                show_scalar_bar=False,
                clim=clim,
                ambient=ambient,
                smooth_shading=True,
                lighting=True
            )
            
        else:
            raise ValueError("Roatation axis is not correct")

        pl.show(auto_close=False)
        image = Image.fromarray(pl.image[:, 128:-128, :])
        image.save(save_path + "_{:s}_{:03d}.png".format(rotation_axis, i))

    pl.close()
    pl.deep_clean()