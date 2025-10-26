# Solution
import pytest
import pandas as pd
import requests
from unittest.mock import patch, MagicMock

from my_krml_25942133.data.api import fetch_api_to_csv  # correct import path


@pytest.fixture
def sample_json_list():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]


@pytest.fixture
def sample_json_dict():
    return {"records": [{"id": 1, "value": 10}, {"id": 2, "value": 20}]}


@patch("requests.get")
def test_fetch_api_to_csv_list_response(mock_get, tmp_path, sample_json_list):
    """Test fetching list-based JSON and saving as CSV."""
    mock_response = MagicMock()
    mock_response.json.return_value = sample_json_list
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    save_path = tmp_path / "data.csv"
    df, path = fetch_api_to_csv("http://dummy.url", str(save_path))

    expected_df = pd.DataFrame(sample_json_list)
    pd.testing.assert_frame_equal(df, expected_df)
    assert path == str(save_path)
    assert save_path.exists()


@patch("requests.get")
def test_fetch_api_to_csv_dict_response(mock_get, tmp_path, sample_json_dict):
    """Test fetching dict-based JSON with single list key."""
    mock_response = MagicMock()
    mock_response.json.return_value = sample_json_dict
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    save_path = tmp_path / "data.csv"
    df, path = fetch_api_to_csv("http://dummy.url", str(save_path))

    expected_df = pd.DataFrame(sample_json_dict["records"])
    pd.testing.assert_frame_equal(df, expected_df)
    assert path == str(save_path)
    assert save_path.exists()


@patch("requests.get")
def test_fetch_api_to_csv_invalid_json(mock_get, tmp_path):
    """Test JSON that cannot be converted cleanly (nested dict)."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"meta": {"count": 1}, "data": {"id": 1, "value": 100}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    save_path = tmp_path / "nested.csv"
    df, path = fetch_api_to_csv("http://dummy.url", str(save_path))

    assert isinstance(df, pd.DataFrame)
    assert path == str(save_path)


@patch("requests.get")
def test_fetch_api_to_csv_http_error(mock_get, tmp_path):
    """Test if HTTPError is raised when request fails."""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")
    mock_get.return_value = mock_response

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_api_to_csv("http://bad.url", str(tmp_path / "fail.csv"))
