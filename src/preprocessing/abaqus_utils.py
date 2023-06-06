import numpy as np
import pandas as pd
from io import StringIO


def get_point_cloud(
    inp_file_path: str
) -> pd.DataFrame:
    node_lines = []
    with open(inp_file_path, "r") as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith('*Node'):
                node_start = i
                break

        for i, line in enumerate(lines[node_start+1:]):
            if line.startswith('*'):
                node_end = node_start + i
                break

        node_lines = lines[node_start+1: node_end+1]

    return pd.read_csv(
        StringIO("\n".join(node_lines)),
        names=["Node", "X", "Y", "Z"]
    )


def get_nodes_and_pressure(df: pd.DataFrame) -> np.ndarray:
    df["Node"] = pd.to_numeric(
        df["Node Label"], errors='coerce')
    df["Pressure"] = pd.to_numeric(
        df["CPRESS     General_Contact_Domain"], errors='coerce')
    return df[["Node", "Pressure"]]


def get_ordered_result(
    inp_file_path: str,
    result_path: str
) -> pd.DataFrame:
    points = get_point_cloud(inp_file_path)
    result = pd.read_csv(result_path, skipinitialspace=True)
    clean_result = get_nodes_and_pressure(result)
    return points.merge(clean_result, on="Node", how="outer").fillna(0)
