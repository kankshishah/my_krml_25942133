# test api.py
import pytest
import pandas as pd
from unittest.mock import patch, Mock
from my_krml_25942133.data.api import fetch_api_to_csv  

@pytest.fixture
def mock_kraken_response():
    # Example OHLC data (nested list like Kraken API)
    return {
        "error": [],
        "result": {
            "SOLUSD": [
                [1762048800, "100", "105", "95", "102", "101", "5000", 10],
                [1762052400, "102", "108", "101", "107", "105", "4500", 8]
            ],
            "last": 1762052400
        }
    }

@patch("requests.get")
def test_fetch_api_to_csv_full(mock_get, mock_kraken_response, tmp_path):
    # Mock the API response
    mock_resp = Mock()
    mock_resp.json.return_value = mock_kraken_response
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    save_path = tmp_path / "test.csv"
    df, path = fetch_api_to_csv(
        url="https://api.kraken.com/0/public/OHLC?pair=SOLUSD&interval=60",
        save_path=str(save_path),
        latest_only=False,
        since_hours=24
    )

    # Check DataFrame shape
    assert df.shape == (2, 8)
    # Check column names
    expected_cols = ["time", "open", "high", "low", "close", "vwap", "volume", "count"]
    assert list(df.columns) == expected_cols
    # Check types
    assert pd.api.types.is_datetime64_any_dtype(df["time"])
    for col in ["open", "high", "low", "close", "vwap", "volume"]:
        assert pd.api.types.is_float_dtype(df[col])

@patch("requests.get")
def test_fetch_api_to_csv_latest_only(mock_get, mock_kraken_response, tmp_path):
    # Mock the API response
    mock_resp = Mock()
    mock_resp.json.return_value = mock_kraken_response
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    save_path = tmp_path / "latest.csv"
    df, path = fetch_api_to_csv(
        url="https://api.kraken.com/0/public/OHLC?pair=SOLUSD&interval=60",
        save_path=str(save_path),
        latest_only=True,
        since_hours=24
    )

    # Should only have one row
    assert df.shape[0] == 1
    # The row should match the last entry in the mock data
    assert df.iloc[0]["close"] == 107.0

@patch("requests.get")
def test_fetch_api_to_csv_invalid_response(mock_get, tmp_path):
    # Return invalid structure
    mock_resp = Mock()
    mock_resp.json.return_value = {"unexpected": "data"}
    mock_resp.raise_for_status = Mock()
    mock_get.return_value = mock_resp

    save_path = tmp_path / "fail.csv"

    with pytest.raises(ValueError):
        fetch_api_to_csv(
            url="https://api.kraken.com/0/public/OHLC?pair=SOLUSD&interval=60",
            save_path=str(save_path),
            latest_only=True
        )
