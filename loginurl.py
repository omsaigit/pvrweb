import webbrowser
from kite_trade import get_enctoken

def open_kite_login_url():
    url = "https://kite.zerodha.com/login"
    webbrowser.open(url)
    print(f"Opened login URL: {url}")

# Example usage to get enctoken (request token)
def get_kite_enctoken(userid, password, twofa):
    return get_enctoken(userid, password, twofa)