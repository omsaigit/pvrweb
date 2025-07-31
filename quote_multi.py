from kiteconnect import KiteConnect
import json
with open('config.json') as f:
    config = json.load(f)
api_key = config['kite_api_key']
access_token = config['access_token']
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Multiple instruments in list format
instruments = ["NSE:INFY", "NSE:TCS", "NSE:HDFCBANK"]
quotes = kite.quote(instruments)
print(quotes)
for symbol, data in quotes.items():
    print(symbol, data['last_price'])
