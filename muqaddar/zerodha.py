import requests
import pandas as pd
from datetime import datetime

# ==============================================================================

# Zerodha API details
token = 738561  # Replace with the correct instrument token
timeframe = "minute"  # Valid timeframes: 'minute', 'day', 'hour', etc.
sdt = "2015-02-02"  # Start date in YYYY-MM-DD format
edt = "2015-04-02"  # End date in YYYY-MM-DD format
enctoken = "+CRQvmeXXkVqfaBpCEEJrqwokY4GYMf4XXhTyRfxsxYyjLDi29/SIP1/slyLlDumFMUu0gC9dXqOm+UlBiA9D/B0jlHpJIpqFP7vmB6PN0LCSmqGu7bOfw=="  # Replace with your valid enctoken

# ==============================================================================

# Headers and URL setup
headers = {
    "Authorization": f"enctoken {enctoken}"
}
url = f"https://kite.zerodha.com/oms/instruments/historical/{token}/{timeframe}"

# Parameters for the API request
params = {
    "oi": 1,  # Include Open Interest data
    "from": sdt,
    "to": edt
}

# ==============================================================================

# Fetching data
try:
    # Making the request
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
    
    # Extracting data
    data = response.json().get("data", {}).get("candles", [])
    
    # Check if data is empty
    if not data:
        print("No data available for the specified parameters.")
    else:
        # Convert to DataFrame
        df = pd.DataFrame(data, columns=["datetime", "open", "high", "low", "close", "volume", "oi"])
        df["datetime"] = pd.to_datetime(df["datetime"])  # Convert datetime strings to datetime objects
        
        # Display data
        print(df.head())  # Display first few rows
        print(f"Total records fetched: {len(df)}")
        
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
except KeyError as e:
    print(f"Unexpected response structure: {e}")
