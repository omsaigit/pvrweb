from flask import Flask, render_template, jsonify, request
from kite_trade import *
from datetime import datetime, timedelta
import json
import time
import threading
import os
from quote import get_quote

app = Flask(__name__)

# Global variables to store data
candles_data = []
hvd = "0"
hr = 0
cv = 0
ltp = 0
current_time = ""
volume_condition = False
hv = 0
is_market_hours = False

# Configuration variables (now configurable)
candles = 25
instrument_token = 14283010
ts = 'NFO:NIFTY25JUL24800CE'

# Load configuration with environment variable fallback
try:
    with open('config.json') as f:
        data = json.load(f)
    enctoken = data.get("AK1099", os.getenv('KITE_ENCTOKEN'))
except Exception as e:
    print(f"Error loading config.json: {e}")
    enctoken = os.getenv('KITE_ENCTOKEN')

# Initialize KiteApp only if enctoken is available
kite = None
if enctoken:
    try:
        kite = KiteApp(enctoken=enctoken)
        print("KiteApp initialized successfully")
    except Exception as e:
        print(f"Error initializing KiteApp: {e}")
else:
    print("Warning: No enctoken available. API calls will fail.")

def get_last_trading_session_end():
    """Get the end time of the last trading session (3:30 PM)"""
    now = datetime.now()
    
    # If current time is before 9:15 AM, get yesterday's session
    if now.hour < 9 or (now.hour == 9 and now.minute < 15):
        # Get yesterday's 3:30 PM
        yesterday = now - timedelta(days=1)
        return yesterday.replace(hour=15, minute=30, second=0, microsecond=0)
    else:
        # Get today's 3:30 PM
        return now.replace(hour=15, minute=30, second=0, microsecond=0)

def is_market_open():
    """Check if market is currently open (9:15 AM to 3:30 PM, Monday to Friday)"""
    now = datetime.now()
    
    # Check if it's a weekday (Monday = 0, Sunday = 6)
    if now.weekday() >= 5:  # Saturday or Sunday
        return False
    
    # Market hours: 9:15 AM to 3:30 PM
    market_start = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_end = now.replace(hour=15, minute=30, second=0, microsecond=0)
    
    return market_start <= now <= market_end

def get_instrument_token_from_ts(trading_symbol):
    """Get instrument token from trading symbol using get_quote"""
    try:
        quote_data = get_quote(trading_symbol)
        if quote_data and trading_symbol in quote_data:
            return quote_data[trading_symbol]['instrument_token']
        else:
            print(f"Could not find instrument token for {trading_symbol}")
            return None
    except Exception as e:
        print(f"Error getting instrument token for {trading_symbol}: {e}")
        return None

def get_initial_quote():
    global minus_volume, ltp
    try:
        if kite is None:
            print("KiteApp not initialized, using dummy data")
            minus_volume = 1000000
            ltp = 50.0
            return
            
        q = get_quote(ts)
        minus_volume = q[ts]['volume']
        ltp = q[ts]['last_price']
        print(f"Initial Volume: {minus_volume}, Initial LTP: {ltp}")
    except Exception as e:
        print(f"Error getting initial quote: {e}")
        minus_volume = 1000000  # Default values for demo
        ltp = 50.0

def get_current_ltp():
    """Get current LTP from quote API"""
    global ltp
    try:
        if kite is None:
            # Return dummy data for demo
            return ltp if ltp > 0 else 50.0
            
        q = get_quote(ts)
        ltp = q[ts]['last_price']
        return ltp
    except Exception as e:
        print(f"Error getting current LTP: {e}")
        return ltp if ltp > 0 else 50.0  # Return existing LTP or default

def format_volume(volume):
    """Format volume in K and M format"""
    if volume >= 1_000_000:
        return f"{volume/1_000_000:.2f}M"
    elif volume >= 1_000:
        return f"{volume/1_000:.2f}K"
    else:
        return str(volume)

def past_candles(start_time, end_time):
    global candles_data, hvd, hr, hv, ltp
    try:
        if kite is None:
            print("KiteApp not initialized, generating dummy candle data")
            # Generate dummy candle data for demo
            candles_data = []
            base_price = 50.0
            base_volume = 1000000
            
            for i in range(candles):
                candle_time = start_time + timedelta(minutes=i)
                open_price = base_price + (i * 0.5) + (i % 3 - 1) * 2
                high_price = open_price + 3 + (i % 5)
                low_price = open_price - 2 - (i % 3)
                close_price = open_price + (i % 2 - 0.5) * 2
                volume = base_volume + (i * 50000) + (i % 7) * 100000
                
                candle = {
                    'date': candle_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(close_price, 2),
                    'volume': volume,
                    'range': round(high_price - low_price, 2),
                    'volume_formatted': format_volume(volume)
                }
                candles_data.append(candle)
            
            # Calculate HVD and HR
            if candles_data:
                hv_candle = max(candles_data, key=lambda x: x['volume'])
                hv = hv_candle['volume']
                hvd = format_volume(hv)

                hr_candle = max(candles_data, key=lambda x: x['range'])
                hr = round(hr_candle['range'], 2)
                
                # Set LTP from the last candle
                ltp = candles_data[-1]['close']
                
                print(f"Generated dummy candles - HVD: {hvd}, HR: {hr}, LTP: {ltp}")
            return
            
        print(f"Fetching candles for instrument_token: {instrument_token}")
        print(f"Time range: {start_time.strftime('%Y-%m-%d %H:%M:%S')} to {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        candles_data = kite.historical_data(
            instrument_token,
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'minute',
            False
        )

        print(f"Received {len(candles_data) if candles_data else 0} candles")

        for candle in candles_data:
            if isinstance(candle, dict) and 'high' in candle and 'low' in candle:
                candle['range'] = candle['high'] - candle['low']
            # Format volume for display
            if isinstance(candle, dict) and 'volume' in candle:
                candle['volume_formatted'] = format_volume(candle['volume'])

        if candles_data:
            hv_candle = max((candle for candle in candles_data if 'volume' in candle), key=lambda x: x['volume'])
            hv = hv_candle['volume']
            vol = hv_candle['volume']
            hvd = format_volume(vol)

            hr_candle = max((candle for candle in candles_data if 'range' in candle), key=lambda x: x['range'])
            hr = round(hr_candle['range'], 2)
            
            # Set LTP from the last candle
            ltp = candles_data[-1]['close']
            
            print(f"Processed candles - HVD: {hvd}, HR: {hr}, LTP: {ltp}")
        else:
            print("No candles data received")
    except Exception as e:
        print(f"Error in past_candles: {e}")
        import traceback
        traceback.print_exc()

def update_data():
    global cv, ltp, current_time, volume_condition, minus_volume, is_market_hours
    while True:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            # Check if market is open
            is_market_hours = is_market_open()
            
            if is_market_hours:
                # Market is open - update real-time data
                if now.second == 0:
                    # Update candles data every minute
                    end_time = now - timedelta(minutes=1)
                    start_time = end_time - timedelta(minutes=candles)
                    past_candles(start_time, end_time)
                    
                    # Update minus_volume
                    try:
                        q = get_quote(ts)
                        minus_volume = q[ts]['volume']
                    except Exception as e:
                        print(f"Error updating minus_volume: {e}")
                
                # Update real-time data every second
                try:
                    if kite is None:
                        # Use dummy data for demo
                        cv = 243000 + (now.second * 1000)  # Simulate changing volume
                        ltp = 60.3 + (now.second % 10) * 0.1  # Simulate changing price
                        volume_condition = cv >= hv
                    else:
                        q = get_quote(ts)
                        cv = q[ts]['volume'] - minus_volume
                        ltp = q[ts]['last_price']
                        volume_condition = cv >= hv
                    print(f"Real-time update - CV: {cv}, LTP: {ltp}")
                except Exception as e:
                    print(f"Error updating real-time data: {e}")
                    # Try to get LTP separately if volume update fails
                    ltp = get_current_ltp()
            else:
                # Market is closed - show last 25 minutes of previous trading session
                if now.minute % 5 == 0 and now.second == 0:  # Update every 5 minutes
                    # Get the end of last trading session (3:30 PM)
                    session_end = get_last_trading_session_end()
                    
                    # Calculate start time for last 25 minutes of trading
                    start_time = session_end - timedelta(minutes=candles)
                    end_time = session_end
                    
                    print(f"Fetching historical data: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
                    past_candles(start_time, end_time)
                    
                    # Set current volume to 0 during non-market hours
                    cv = 0
                    volume_condition = False
                    
                    # Try to get last known LTP from historical data
                    if candles_data and len(candles_data) > 0:
                        ltp = candles_data[-1]['close']
                        print(f"LTP from historical data: {ltp}")
                    else:
                        ltp = 0
                        print("No historical data available for LTP")
            
            time.sleep(1)
        except Exception as e:
            print(f"Error in update_data: {e}")
            time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'App is working!',
        'kite_available': kite is not None,
        'current_time': datetime.now().strftime("%H:%M:%S")
    })

@app.route('/api/data')
def get_data():
    return jsonify({
        'candles_data': candles_data,
        'hvd': hvd,
        'hr': hr,
        'cv': cv,
        'cv_formatted': format_volume(cv),
        'ltp': ltp,
        'current_time': current_time,
        'volume_condition': volume_condition,
        'hv': hv,
        'instrument_symbol': ts,
        'is_market_hours': is_market_hours
    })

@app.route('/api/realtime_data')
def get_realtime_data():
    """API endpoint for real-time data that updates every second"""
    return jsonify({
        'cv': cv,
        'cv_formatted': format_volume(cv),
        'ltp': ltp,
        'current_time': current_time,
        'volume_condition': volume_condition,
        'is_market_hours': is_market_hours
    })

@app.route('/api/table_data')
def get_table_data():
    """API endpoint for table data that updates only at 0th second"""
    return jsonify({
        'candles_data': candles_data,
        'hvd': hvd,
        'hr': hr,
        'hv': hv,
        'instrument_symbol': ts,
        'is_market_hours': is_market_hours
    })

@app.route('/api/update_config', methods=['POST'])
def update_config():
    global candles, instrument_token, ts, minus_volume, is_market_hours
    
    try:
        data = request.get_json()
        
        # Validate input
        if not all(key in data for key in ['candles', 'ts']):
            return jsonify({'success': False, 'error': 'Missing required parameters'})
        
        new_candles = int(data['candles'])
        new_ts = str(data['ts'])
        
        # Validate ranges
        if new_candles < 1 or new_candles > 100:
            return jsonify({'success': False, 'error': 'Candles must be between 1 and 100'})
        
        # Get instrument token automatically from trading symbol
        new_instrument_token = get_instrument_token_from_ts(new_ts)
        if new_instrument_token is None:
            return jsonify({'success': False, 'error': f'Could not get instrument token for {new_ts}'})
        
        # Update configuration
        candles = new_candles
        instrument_token = new_instrument_token
        ts = new_ts
        
        print(f"Updated configuration: candles={candles}, instrument_token={instrument_token}, ts={ts}")
        
        # Reinitialize with new configuration based on market hours
        is_market_hours = is_market_open()
        
        if is_market_hours:
            # Market is open - initialize with current time data
            get_initial_quote()
            curr_time = datetime.now()
            end_time = curr_time - timedelta(minutes=1)
            start_time = end_time - timedelta(minutes=candles)
            print(f"Reinitializing with live data: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
        else:
            # Market is closed - initialize with last 25 minutes of previous session
            session_end = get_last_trading_session_end()
            start_time = session_end - timedelta(minutes=candles)
            end_time = session_end
            print(f"Reinitializing with historical data: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
        
        past_candles(start_time, end_time)
        
        return jsonify({
            'success': True, 
            'instrument_token': instrument_token,
            'message': f'Configuration updated successfully. Instrument token: {instrument_token}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_instrument_token/<trading_symbol>')
def get_instrument_token_api(trading_symbol):
    """API endpoint to get instrument token for a trading symbol"""
    try:
        token = get_instrument_token_from_ts(trading_symbol)
        if token:
            return jsonify({'success': True, 'instrument_token': token})
        else:
            return jsonify({'success': False, 'error': f'Could not get instrument token for {trading_symbol}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/refresh_candles')
def refresh_candles():
    """API endpoint to manually refresh candle data for debugging"""
    global candles_data, hvd, hr, hv
    
    try:
        is_market_hours = is_market_open()
        
        if is_market_hours:
            # Market is open - get current time data
            curr_time = datetime.now()
            end_time = curr_time - timedelta(minutes=1)
            start_time = end_time - timedelta(minutes=candles)
            print(f"Manual refresh - Live data: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
        else:
            # Market is closed - get last 25 minutes of previous session
            session_end = get_last_trading_session_end()
            start_time = session_end - timedelta(minutes=candles)
            end_time = session_end
            print(f"Manual refresh - Historical data: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
        
        past_candles(start_time, end_time)
        
        return jsonify({
            'success': True,
            'candles_count': len(candles_data) if candles_data else 0,
            'hvd': hvd,
            'hr': hr,
            'is_market_hours': is_market_hours,
            'time_range': f"{start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_ltp')
def get_ltp_api():
    """API endpoint to get current LTP for debugging"""
    try:
        current_ltp = get_current_ltp()
        return jsonify({
            'success': True,
            'ltp': current_ltp,
            'instrument_symbol': ts,
            'is_market_hours': is_market_hours
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Initialize data based on market hours
    is_market_hours = is_market_open()
    
    if is_market_hours:
        # Market is open - initialize with current time data
        get_initial_quote()
        curr_time = datetime.now()
        end_time = curr_time - timedelta(minutes=1)
        start_time = end_time - timedelta(minutes=candles)
        print(f"Initializing with live data: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
    else:
        # Market is closed - initialize with last 25 minutes of previous session
        session_end = get_last_trading_session_end()
        start_time = session_end - timedelta(minutes=candles)
        end_time = session_end
        print(f"Initializing with historical data: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
    
    past_candles(start_time, end_time)
    
    # Start background thread for data updates
    update_thread = threading.Thread(target=update_data, daemon=True)
    update_thread.start()
    
    app.run(debug=True, host='0.0.0.0', port=5001) 