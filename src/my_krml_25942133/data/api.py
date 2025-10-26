import pandas as pd
import requests

def fetch_api_to_csv(url, save_path):
"""Fetch data from an API endpoint, convert it to a DataFrame, and save as CSV.

Parameters
----------
url : str
    API endpoint URL to fetch data from.
save_path : str
    File path to save the resulting DataFrame as a CSV file.

Returns
-------
pd.DataFrame
    DataFrame created from the JSON response.
str
    File path where the CSV was saved.
"""

# Fetch data from API
response = requests.get(url)
response.raise_for_status()  # Raises HTTPError for failed requests
data = response.json()

# Convert JSON to DataFrame (auto-detects structure)
if isinstance(data, dict) and len(data) == 1 and isinstance(next(iter(data.values())), list):
    df = pd.DataFrame(next(iter(data.values())))
elif isinstance(data, list):
    df = pd.DataFrame(data)
else:
    df = pd.json_normalize(data)

# Save DataFrame to CSV
df.to_csv(save_path, index=False)
print(f"Data saved at: {save_path}")

return df, save_path

