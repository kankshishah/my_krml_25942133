import pandas as pd
import requests
import time

def fetch_api_to_csv(url, save_path, latest_only=False, since_hours=24):
    """
    Fetch OHLC data from Kraken API, convert it to a DataFrame, and save as CSV.
    
    Parameters:
    - url: str, Kraken OHLC API endpoint without 'since' parameter
    - save_path: str, path to save CSV
    - latest_only: bool, if True, keep only the latest row
    - since_hours: int, fetch data from this many hours ago
    """
    
    # Calculate 'since' UNIX timestamp
    since_timestamp = int(time.time()) - since_hours*60*60
    full_url = f"{url}&since={since_timestamp}" if "since=" not in url else url

    # Fetch data
    response = requests.get(full_url)
    response.raise_for_status()
    data = response.json()

    # Extract OHLC data
    pair_key = next((k for k in data["result"].keys() if k != "last"), None)
    if pair_key is None:
        raise ValueError("No valid trading pair found in API response.")
    ohlc_data = data["result"][pair_key]

    # Define column names
    columns = ["time", "open", "high", "low", "close", "vwap", "volume", "count"]

    # Convert to DataFrame
    df = pd.DataFrame(ohlc_data, columns=columns)

    # Convert timestamp to datetime
    df["time"] = pd.to_datetime(df["time"], unit="s")

    # Convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "vwap", "volume"]
    df[numeric_cols] = df[numeric_cols].astype(float)

    # Keep only the latest row if required
    if latest_only:
        df = df.iloc[[-1]]

    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"Data saved at: {save_path}")

    return df, save_path
