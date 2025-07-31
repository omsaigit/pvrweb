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
    url = f'https://api.kite.trade/quote?i={instrument}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        print('Error:', response.status_code, response.text)
        return None

# Example usage:
if __name__ == "__main__":
    data = get_quote('NSE:INFY')
    print(data)
