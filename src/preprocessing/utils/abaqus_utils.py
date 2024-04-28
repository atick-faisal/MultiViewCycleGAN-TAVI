import pandas as pd
from io import StringIO


def _get_point_cloud_from_inp_file(inp_file_path: str) -> pd.DataFrame:
    """
    Reads an input file in 'inp' format and extracts the point cloud data.

    Parameters:
        inp_file_path (str): The file path of the input file.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted point cloud data with columns ['Node', 'X', 'Y', 'Z'].
    """
    node_lines = []
    with open(inp_file_path, "r") as f:
        lines = f.readlines()

        # Find the starting line of the '*Node' section
        for i, line in enumerate(lines):
            if line.startswith("*Node"):
                node_start = i
                break

        # Find the ending line of the '*Node' section
        for i, line in enumerate(lines[node_start + 1 :]):
            if line.startswith("*"):
                node_end = node_start + i
                break

        # Extract the lines containing node data
        node_lines = lines[node_start + 1 : node_end + 1]

    # Convert the extracted node data to a DataFrame
    return pd.read_csv(StringIO("\n".join(node_lines)), names=["Node", "X", "Y", "Z"])


def _get_clean_result(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Extracts the nodes and corresponding pressure values from a DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the result data.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted node and pressure data with columns ['Node', 'Pressure'].
    """
    # Convert the 'Node Label' and 'CPRESS     General_Contact_Domain' columns to numeric
    df["Node"] = pd.to_numeric(df["Node Label"], errors="coerce")
    df["Value"] = pd.to_numeric(df[column_name], errors="coerce")

    # Select only the 'Node' and 'Pressure' columns
    return df[["Node", "Value"]]


def get_pressure_result(inp_file_path: str, pressure_path: str) -> pd.DataFrame:
    """
    Reads an input file and a result file, and merges the extracted point cloud data with the result data.

    Parameters:
        inp_file_path (str): The file path of the input file in 'inp' format.
        result_path (str): The file path of the result file.

    Returns:
        pd.DataFrame: A DataFrame containing the merged data with columns ['Node', 'X', 'Y', 'Z', 'Pressure'].
    """
    # Extract the point cloud data from the input file
    points = _get_point_cloud_from_inp_file(inp_file_path)

    # Read the result data from the result file
    result = pd.read_csv(pressure_path, skipinitialspace=True)

    # Extract the nodes and pressure data from the result DataFrame
    clean_result = _get_clean_result(result, "CPRESS     General_Contact_Domain")

    # Merge the point cloud data with the result data based on the 'Node' column
    merged_data = points.merge(clean_result, on="Node", how="inner").fillna(0)

    return merged_data


def get_stress_result(inp_file_path: str, stress_path: str) -> pd.DataFrame:
    """
    Reads an input file and a result file, and merges the extracted point cloud data with the result data.

    Parameters:
        inp_file_path (str): The file path of the input file in 'inp' format.
        result_path (str): The file path of the result file.

    Returns:
        pd.DataFrame: A DataFrame containing the merged data with columns ['Node', 'X', 'Y', 'Z', 'Pressure'].
    """
    # Extract the point cloud data from the input file
    points = _get_point_cloud_from_inp_file(inp_file_path)

    # Read the result data from the result file
    result = pd.read_csv(stress_path, skipinitialspace=True)

    # Extract the nodes and pressure data from the result DataFrame
    clean_result = _get_clean_result(result, "S-Mises")

    # Merge the point cloud data with the result data based on the 'Node' column
    merged_data = points.merge(clean_result, on="Node", how="inner").fillna(0)

    return merged_data


def extract_part(data, part_name):
    """
    Extracts a part from a string containing Abaqus input file data.

    Args:
        data: The string containing the Abaqus input file data.
        part_name: The name of the part to extract.

    Returns:
        A string containing the extracted part data.
    """
    start_line = f"*Part, name={part_name}"
    end_line = "*End Part"
    in_part = False
    part_data = []
    for line in data.splitlines():
        if line.startswith(start_line):
            in_part = True
        elif line == end_line and in_part:
            in_part = False
            break
        if in_part:
            part_data.append(line)
    return "\n".join(part_data)
