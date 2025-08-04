from kiteconnect import KiteConnect
import json
import os

api_key = "gs3dacf2honsskjw"
api_secret = "xgkm43b7fcquzrd1njsjky2t7qb1rax3"
request_token = "a6kgkpvBBfNpOoVl9wUROHxl3xcsXeAi"
with open('config.json', 'r') as file:
    config_data = json.load(file)
kite = KiteConnect(api_key=api_key)

data = kite.generate_session(request_token=request_token, api_secret=api_secret)

access_token = data["access_token"]


config_data["access_token"] = access_token

with open('config.json', 'w') as file:
    json.dump(config_data, file, indent=2)

print("Access Token:", access_token)
