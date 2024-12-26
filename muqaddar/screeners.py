import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import quote

url = "https://chartink.com/screener/process"

# Example simplified condition 
condition = {
    "scan_clause": quote("(daily+macd+line(+26+,+12+,+9+)+>+daily+macd+signal(+26+,+12+,+9+))")
}


with requests.session() as s:
    try:
        # Fetch the CSRF token
        r_data = s.get(url)
        r_data.raise_for_status()  # Ensure the request is successful
        soup = bs(r_data.content, "lxml")
        meta = soup.find("meta", {"name": "csrf-token"})["content"]

        # Prepare headers
        header = {"x-csrf-token": meta}

        # Send the POST request
        response = s.post(url, headers=header, data=condition)
        response.raise_for_status()  # Ensure the POST request is successful
        
        # Debug: Print raw response text to understand what Chartink is returning
        print(response.text)  # This will help us debug
        
        # Parse the JSON response
        data = response.json()
        
        # Check if 'data' exists and is not empty
        if 'data' in data and data['data']:
            stock_list = pd.DataFrame(data["data"])
            print(stock_list)
        else:
            print("No data returned.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
