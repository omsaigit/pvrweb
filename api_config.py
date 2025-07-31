from kite_trade import *
from api import *
import pyotp

# Step 1: Read existing JSON data from config.json
with open('config.json', 'r') as file:
    config_data = json.load(file)
ud = user_details()
for uses in ud['users']:
    token =uses['entoken']
    kite = KiteApp(enctoken=token)
    profile =kite.profile()
    if profile:
        if profile['user_id']==uses['user_id']:
            
            balance = kite.margins()["equity"]['available']["live_balance"]
            
            config_data[uses['user_id']] = token
            with open('config.json', 'w') as file:
                json.dump(config_data, file, indent=2)
                print('Config file updated successfully.',uses['user_name'],balance)
    else:
        with open('users_details.json') as f:
            udg = json.load(f)
            for ud in udg:
                if ud['user_id']==uses['user_id']:                   
                    if len(uses['secret_key'])>5:
                        totp = pyotp.TOTP(uses['secret_key'])
                        twofa = totp.now()
                        print(ud['user_id']," TOTP:",twofa)
                    else:
                        twofa = input('Please Enter TOTP for '+ud['user_id']+' :')
                    if twofa:
                        get_token = get_enctoken(ud['user_id'], ud['password'], twofa)
                        kite_new = KiteApp(enctoken=get_token)
                        marginr = dict(kite_new.margins())
                        balancer = int(marginr["equity"]['available']["live_balance"])
                        try:
                            update_token_api(ud['user_id'],get_token,balancer)
                            config_data[ud['user_id']] = get_token
                            with open('config.json', 'w') as file:
                                json.dump(config_data, file, indent=2)
                                print('Config file updated successfully.')
                        except:
                            print("Failed to Update Token",ud['user_id'])
                    

