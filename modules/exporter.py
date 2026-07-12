"""
Exporter Module

Exports ranked candidates to:
1. CSV
2. JSON
"""

import os
import json
import pandas as pd
import numpy as np


def convert_numpy(obj):
    """
    Convert NumPy data types into native Python types.
    """
    if isinstance(obj, np.integer):
        return int(obj)

    if isinstance(obj, np.floating):
        return float(obj)

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def export_to_csv(candidates, output_folder):
    """
    Export ranked candidates to CSV.

    Args:
        candidates (list): List of ranked candidate dictionaries.
        output_folder (str): Output directory.
    """

    csv_file = os.path.join(output_folder, "ranked_candidates.csv")

    df = pd.DataFrame(candidates)

    df.to_csv(csv_file, index=False)

    print(f"CSV exported successfully: {csv_file}")


def export_to_json(candidates, output_folder):
    """
    Export ranked candidates to JSON.

    Args:
        candidates (list): List of ranked candidate dictionaries.
        output_folder (str): Output directory.
    """

    json_file = os.path.join(output_folder, "ranked_candidates.json")

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(
            candidates,
            file,
            indent=4,
            ensure_ascii=False,
            default=convert_numpy
        )

    print(f"JSON exported successfully: {json_file}")

def export_results(candidates, output_folder):
    """
    Export ranked candidates to both CSV and JSON.

    Args:
        candidates (list): Ranked candidate list.
        output_folder (str): Output directory.
    """

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    export_to_csv(candidates, output_folder)

    export_to_json(candidates, output_folder)

    print("\nAll results exported successfully!")