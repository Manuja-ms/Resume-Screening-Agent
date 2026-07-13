import json
import numpy as np
import pandas as pd

from modules.exporter import (
    convert_numpy,
    export_to_csv,
    export_to_json,
    export_results
)


def sample_candidates():
    return [
        {
            "Name": "Alice",
            "Score": 92.5,
            "Skills": ["Python", "SQL"],
            "Experience": 3
        },
        {
            "Name": "Bob",
            "Score": 85.0,
            "Skills": ["Java", "Spring"],
            "Experience": 2
        }
    ]


def test_convert_numpy_integer():
    assert convert_numpy(np.int64(10)) == 10


def test_convert_numpy_float():
    assert convert_numpy(np.float64(9.5)) == 9.5


def test_convert_numpy_array():
    arr = np.array([1, 2, 3])
    assert convert_numpy(arr) == [1, 2, 3]


def test_export_to_csv(tmp_path):
    candidates = sample_candidates()

    export_to_csv(candidates, tmp_path)

    csv_file = tmp_path / "ranked_candidates.csv"

    assert csv_file.exists()

    df = pd.read_csv(csv_file)

    assert len(df) == 2
    assert "Name" in df.columns
    assert "Score" in df.columns
    assert df.iloc[0]["Name"] == "Alice"


def test_export_to_json(tmp_path):
    candidates = sample_candidates()

    export_to_json(candidates, tmp_path)

    json_file = tmp_path / "ranked_candidates.json"

    assert json_file.exists()

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["Name"] == "Alice"
    assert data[1]["Experience"] == 2


def test_export_results(tmp_path):
    candidates = sample_candidates()

    export_results(candidates, tmp_path)

    csv_file = tmp_path / "ranked_candidates.csv"
    json_file = tmp_path / "ranked_candidates.json"

    assert csv_file.exists()
    assert json_file.exists()


def test_export_empty_candidates(tmp_path):
    candidates = []

    export_results(candidates, tmp_path)

    csv_file = tmp_path / "ranked_candidates.csv"
    json_file = tmp_path / "ranked_candidates.json"

    assert csv_file.exists()
    assert json_file.exists()

    df = pd.read_csv(csv_file)
    assert df.empty

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == []