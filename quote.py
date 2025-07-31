import requests
import json

# Load API key and access token from config.json
with open('config.json') as f:
    config = json.load(f)
api_key = config['kite_api_key']
access_token = config['access_token']

headers = {
    'X-Kite-Version': '3',
    'Authorization': f'token {api_key}:{access_token}'
}

def get_quote(instrument):
    """Get quote data for a given instrument symbol, e.g. 'NSE:INFY'"""
    try:
        url = f'https://api.kite.trade/quote?i={instrument}'
        print(f"Making API request to: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data keys: {list(data.keys()) if data else 'None'}")
            return data.get('data')
        else:
            print(f'API Error: {response.status_code}, Response: {response.text}')
            return None
    except requests.exceptions.Timeout:
        print(f"Timeout error while fetching quote for {instrument}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error while fetching quote for {instrument}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while fetching quote for {instrument}: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    data = get_quote('NSE:INFY')
    print(data)
