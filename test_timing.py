#!/usr/bin/env python3
"""
Test script to verify timing improvements and data freshness
"""

import requests
import json
from datetime import datetime, timedelta

def get_ist_time():
    """Get current time in IST (UTC + 5:30)"""
    utc_now = datetime.utcnow()
    ist_time = utc_now + timedelta(hours=5, minutes=30)
    return ist_time

def test_data_freshness():
    """Test the freshness of data from the API"""
    print("=== Testing Data Freshness ===")
    
    # Get current time
    current_time = get_ist_time()
    print(f"Current time (IST): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Test force refresh endpoint
        print("\n1. Testing force refresh endpoint...")
        response = requests.get('http://localhost:5001/api/force_refresh')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Force refresh successful")
            print(f"   Time range: {data.get('time_range', 'N/A')}")
            print(f"   Current time: {data.get('current_time', 'N/A')}")
            print(f"   Candles count: {data.get('candles_count', 'N/A')}")
        else:
            print(f"❌ Force refresh failed: {response.status_code}")
        
        # Test table data endpoint
        print("\n2. Testing table data endpoint...")
        response = requests.get('http://localhost:5001/api/table_data')
        if response.status_code == 200:
            data = response.json()
            candles_data = data.get('candles_data', [])
            if candles_data:
                latest_candle = candles_data[-1]
                try:
                    # Try different date formats
                    date_str = latest_candle['date']
                    if 'GMT' in date_str:
                        # Handle GMT format
                        candle_time = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT')
                        # Convert to IST (GMT + 5:30)
                        candle_time = candle_time + timedelta(hours=5, minutes=30)
                    else:
                        # Handle standard format
                        candle_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                    
                    time_diff = current_time - candle_time
                    print(f"✅ Table data retrieved")
                    print(f"   Latest candle time: {candle_time.strftime('%H:%M:%S')}")
                    print(f"   Time difference: {time_diff}")
                    print(f"   Lag: {time_diff.total_seconds() / 60:.1f} minutes")
                except Exception as e:
                    print(f"✅ Table data retrieved (date parsing error: {e})")
                    print(f"   Latest candle date: {latest_candle['date']}")
            else:
                print("❌ No candles data available")
        else:
            print(f"❌ Table data failed: {response.status_code}")
        
        # Test real-time data endpoint
        print("\n3. Testing real-time data endpoint...")
        response = requests.get('http://localhost:5001/api/realtime_data')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Real-time data retrieved")
            print(f"   Current time: {data.get('current_time', 'N/A')}")
            print(f"   LTP: {data.get('ltp', 'N/A')}")
            print(f"   CV: {data.get('cv_formatted', 'N/A')}")
        else:
            print(f"❌ Real-time data failed: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the Flask app is running on localhost:5001")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

def test_configuration():
    """Test the current configuration"""
    print("\n=== Testing Configuration ===")
    
    try:
        response = requests.get('http://localhost:5001/test')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ App is running")
            print(f"   Kite available: {data.get('kite_available', 'N/A')}")
            print(f"   Current time: {data.get('current_time', 'N/A')}")
            print(f"   Candles count: {data.get('candles_count', 'N/A')}")
        else:
            print(f"❌ App test failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server")
    except Exception as e:
        print(f"❌ Error during configuration test: {e}")

if __name__ == "__main__":
    print("PVR Trading Dashboard - Timing Test")
    print("=" * 50)
    
    test_configuration()
    test_data_freshness()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nTo reduce lag further:")
    print("1. Use the 'Force Refresh' button on the web interface")
    print("2. The app now updates data every 30 seconds instead of every minute")
    print("3. Historical data is requested with minimal delay")
    print("4. Note: Zerodha API typically has 1-2 minute inherent delay") 