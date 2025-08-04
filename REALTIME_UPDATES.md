# Real-Time Updates - Every Second

## Overview
The PVR Trading Dashboard now updates real-time data every second with improved reliability and visual feedback.

## Key Improvements

### 1. Backend Updates (`web_app.py`)

#### Enhanced Background Thread
- The `update_data()` function now runs continuously in a background thread
- Updates real-time data (CV and LTP) every second during market hours
- Updates candle data every minute (at 0th second)
- Handles both live market data and dummy data modes

#### Improved Real-Time API Endpoint
- `/api/realtime_data` endpoint now fetches fresh data on every request
- Added timestamp for debugging and verification
- Better error handling and fallback mechanisms
- More realistic dummy data variations for testing

#### Key Features:
```python
# Real-time data updates every second
@app.route('/api/realtime_data')
def get_realtime_data():
    # Always fetch fresh data
    # Handle both live and dummy data modes
    # Return timestamp for verification
```

### 2. Frontend Updates (`templates/index.html`)

#### Precise Timing
- Uses `setInterval(updateData, 1000)` for exact 1-second intervals
- Separate handling for real-time data vs table data updates
- Real-time data updates every second
- Table data updates only at the start of each minute

#### Visual Feedback
- Added updating animation for real-time values
- Real-time indicator dot (green pulsing dot) during market hours
- Market status indicator (red/green dot)
- Volume condition highlighting when CV >= HV

#### Error Handling
- Automatic retry logic for failed API calls
- Pause updates after consecutive errors
- Graceful degradation with fallback data

### 3. Visual Indicators

#### Real-Time Indicator
- Green pulsing dot in bottom-right corner
- Only visible during market hours
- Indicates active real-time updates

#### Market Status
- Red dot: Market closed
- Green blinking dot: Market open

#### Volume Condition
- Red background with pulse animation when CV >= HV
- Normal background otherwise

## Testing

### Manual Testing
1. Start the web app: `python web_app.py`
2. Open browser to `http://localhost:5001`
3. Watch the real-time values update every second
4. Check browser console for update logs

### Automated Testing
Run the test script to verify updates:
```bash
python test_realtime.py
```

This will test the API for 10 seconds and show timestamps.

## Configuration

### Real-Time Update Settings
- **Update Frequency**: Every 1 second
- **Table Updates**: Every minute (at 0th second)
- **Indices Updates**: Every 1 second
- **Error Retry**: Pause for 10 seconds after 5 consecutive errors

### Market Hours Detection
- **Market Open**: 9:15 AM to 3:30 PM IST, Monday to Friday
- **Real-time Updates**: Only during market hours
- **Historical Data**: During non-market hours

## Troubleshooting

### Common Issues

1. **Updates not happening every second**
   - Check browser console for errors
   - Verify network connectivity
   - Check if market is open

2. **Dummy data not changing**
   - This is normal in dummy mode
   - Data changes are subtle for realistic simulation

3. **API errors**
   - Check if the web app is running
   - Verify API endpoints are accessible
   - Check server logs for errors

### Debug Information
- Browser console shows update logs
- API responses include timestamps
- Server logs show background thread activity

## Performance Notes

- Real-time updates use minimal bandwidth
- Background thread runs independently
- Frontend handles errors gracefully
- Automatic fallback to cached data on errors 