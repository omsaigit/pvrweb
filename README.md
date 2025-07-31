# PVR Trading Dashboard

A real-time web dashboard for monitoring trading data with automatic updates.

## Features

- **Real-time Data Updates**: 
  - Candles data updates every minute (at 00 seconds)
  - HVD and HR values update every minute
  - CV, LTP, and time update every second
- **Volume Condition Alert**: Visual alert when CV >= HV
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with glassmorphism effects

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have all the required files:
   - `config.json` (with your API configuration)
   - `kite_trade.py`
   - `quote.py`
   - All other supporting files

## Usage

1. Run the web application:
```bash
python web_app.py
```

2. Open your browser and navigate to:
```
http://localhost:5001
```

## Data Display

The dashboard shows:

### Status Cards (Update every second)
- **HVD (Highest Volume)**: Maximum volume in the last 25 minutes
- **HR (Highest Range)**: Maximum price range in the last 25 minutes
- **CV (Current Volume)**: Current volume minus initial volume
- **LTP (Last Traded Price)**: Current market price
- **Current Time**: Real-time clock

### Candles Table (Updates every minute)
- Shows the last 25 minutes of candle data
- Columns: Time, Open, High, Low, Close, Volume, Range

### Volume Condition Alert
- When CV >= HV, the CV card will turn red and pulse
- This indicates a high volume condition that may require attention

## Technical Details

- **Backend**: Flask web server with background threading
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Updates**: RESTful API endpoint `/api/data`
- **Real-time Updates**: JavaScript polling every second
- **Error Handling**: Graceful error handling for API failures

## Market Hours

The application is designed to work during market hours (9:16 AM to 3:30 PM IST). Outside these hours, it will show "Market is closed" message.

## Troubleshooting

1. **No data showing**: Check if your API credentials are correct in `config.json`
2. **Connection errors**: Ensure your internet connection is stable
3. **Port already in use**: Change the port in `web_app.py` if port 5000 is occupied

## Security Note

- The application runs on `0.0.0.0:5001` by default
- For production use, consider using a proper WSGI server and HTTPS
- Keep your API credentials secure and never commit them to version control # pvrweb
