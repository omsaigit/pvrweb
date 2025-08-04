#!/usr/bin/env python3
"""
Test script to verify real-time updates are working every second
"""

import requests
import time
import json
from datetime import datetime

def test_realtime_updates():
    """Test that real-time data updates every second"""
    base_url = "http://localhost:5001"
    
    print("Testing real-time updates every second...")
    print("=" * 50)
    
    # Test for 10 seconds
    for i in range(10):
        try:
            # Get real-time data
            response = requests.get(f"{base_url}/api/realtime_data", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                current_time = datetime.now().strftime("%H:%M:%S")
                
                print(f"[{current_time}] CV: {data.get('cv_formatted', 'N/A')}, "
                      f"LTP: {data.get('ltp', 0):.2f}, "
                      f"Market Open: {data.get('is_market_hours', False)}, "
                      f"Timestamp: {data.get('timestamp', 'N/A')}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Network error: {e}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")
        
        # Wait 1 second
        time.sleep(1)
    
    print("=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_realtime_updates() 