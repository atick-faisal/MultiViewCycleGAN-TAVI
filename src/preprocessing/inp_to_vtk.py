import os
import meshio
import tqdm
from utils import get_file_with_extension

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

DATA_DIR = os.path.join(current_dir, "../../data/dataset")
PATIENTS_DIR = "Patients"


def convert_inp_to_vtk(inp_file_path: str) -> None:
    """
    Converts an input file (.inp) to the VTK format.

    Parameters:
        inp_file_path (str): The path of the input file.

    Returns:
        None

    Example:
        convert_inp_to_vtk('input_file.inp')
    """
    # Read the input file using meshio
    mesh = meshio.read(inp_file_path)

    # Write the mesh to VTK format
    # mesh.write(inp_file_path + ".vtk")
    mesh.write(inp_file_path + ".stl")


def convert_all_inp_files_to_vtk() -> None:
    """
    Converts all input files (.inp) in the dataset to VTK format.

    Parameters:
        None

    Returns:
        None

    Example:
        convert_all_inp_files_to_vtk()
    """
    # Get the path to the patients directory
    patients_path = os.path.join(DATA_DIR, PATIENTS_DIR)

    # Get the list of patients
    patients = os.listdir(patients_path)

    # Iterate over the patients
    for patient in tqdm.tqdm(patients):
        # Get the path to the sizes directory for the current patient
        sizes_path = os.path.join(patients_path, patient)

        # Get the list of sizes for the current patient
        sizes = os.listdir(sizes_path)

        # Iterate over the sizes
        for size in sizes:
            # Get the path to the files directory for the current size
            files_path = os.path.join(sizes_path, size)

            # Get the path of the input file (.inp) in the current size directory
            input_file_path = get_file_with_extension(files_path, ".inp")

            # Convert the input file to STL format
            convert_inp_to_vtk(input_file_path)


if __name__ == "__main__":
    convert_all_inp_files_to_vtk()
