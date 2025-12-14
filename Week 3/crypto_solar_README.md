# 🌞₿ Crypto vs Solar Activity Dashboard

**"I hate not knowing if solar flares crash Bitcoin, so I built this."**

A fascinating dashboard that correlates Bitcoin price movements with solar activity data. Because maybe the universe affects our portfolios more than we think! 

## What It Does

Mashes up two completely unrelated data sources:
- **Bitcoin prices** from CoinGecko API
- **Solar wind activity** from NOAA Space Weather API

Then calculates correlations and visualizes potential cosmic connections to cryptocurrency markets.

## Features

- 📈 Real-time Bitcoin price tracking
- 🌞 Solar wind speed, density, and temperature data
- 🔗 Statistical correlation analysis
- 📊 Interactive charts with dual y-axes
- 🎯 Solar activity level indicators
- 🧠 AI-generated insights

## Quick Start Options

### Option 1: Interactive Streamlit Dashboard (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run crypto_solar_dashboard.py
```

Then open your browser to `http://localhost:8501`

### Option 2: Simple HTML Dashboard

Just open `simple_dashboard.html` in your browser - no installation needed!

## Screenshots

The dashboard includes:
- Bitcoin price charts with trend indicators
- Solar wind speed overlays
- Correlation coefficient calculations
- Activity level gauges
- Statistical significance testing

## Data Sources

- **Bitcoin Data**: CoinGecko API (free, no API key required)
- **Solar Data**: NOAA Space Weather Prediction Center
- **Fallback**: Mock realistic data for demo purposes

## Correlation Metrics

The dashboard calculates Pearson correlation coefficients between:
- Bitcoin price vs Solar wind speed
- Bitcoin price vs Solar wind density  
- Bitcoin price vs Solar wind temperature

Results include:
- Correlation strength (-1 to +1)
- Statistical significance (p-values)
- Interpretation (Strong/Moderate/Weak)

## Fun Insights

- Solar wind normally travels 300-800 km/s
- High solar activity (>600 km/s) is relatively rare
- Correlations are usually weak (as expected!)
- But occasionally you might find surprising patterns...

## Customization

Want to explore other correlations? Easy modifications:

```python
# Add other cryptocurrencies
coins = ['bitcoin', 'ethereum', 'cardano']

# Try different timeframes
days = 90  # 3 months of data

# Add more space weather metrics
# - Geomagnetic storms
# - Solar flare intensity
# - Cosmic ray levels
```

## Technical Details

- **Frontend**: Streamlit + Plotly for interactive charts
- **Backend**: Python with pandas for data processing
- **APIs**: RESTful calls with error handling
- **Statistics**: SciPy for correlation analysis
- **Fallbacks**: Mock data generation for reliability

## Requirements

- Python 3.7+
- Internet connection for live data
- Modern web browser

## Why This Matters

While correlations between Bitcoin and solar activity are likely coincidental, this project demonstrates:
- Creative data mashup techniques
- Real-time API integration
- Statistical analysis visualization
- The joy of exploring unexpected connections!

## Disclaimer

This is for educational and entertainment purposes. Solar flares probably don't affect Bitcoin prices (but wouldn't it be cool if they did?). 

*Not financial advice. Not astronomical advice either.*