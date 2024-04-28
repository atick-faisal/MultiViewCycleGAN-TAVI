import os
import tqdm
from utils import get_file_with_extension, extract_part

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)

DATA_DIR = "/mnt/Data/Datasets/TAVI/"
PATIENTS_DIR = "Patients"


def extract_part_from_inp_files() -> None:
    """
    Extract parts like AORTA or STENT from inp files

    Parameters:
        None

    Returns:
        None

    Example:
        extract_part_from_inp_files()
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
            input_file_path = get_file_with_extension(files_path, "MM.inp")

            # Read input fiel
            with open(input_file_path, "r") as file:
                input_data = file.read()

            # Get aorta
            aorta = extract_part(input_data, "AORTA")
            stent = extract_part(input_data, "STENT")

            # Write Files
            with open(input_file_path + "AORTA_PRE.inp", "w") as output_file:
                output_file.write(aorta)

            with open(input_file_path + "STENT_PRE.inp", "w") as output_file:
                output_file.write(stent)


if __name__ == "__main__":
    extract_part_from_inp_files()
