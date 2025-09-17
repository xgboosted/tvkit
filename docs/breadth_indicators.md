# Nasdaq 100 Breadth Indicators Support

tvkit now supports the following Nasdaq 100 breadth indicators for macro liquidity and market breadth analysis:

## Supported Breadth Indicators

- **INDEX-NDTH**: Nasdaq 100 Stocks Above 200-Day Average
- **INDEX-NDFI**: Nasdaq 100 Stocks Above 50-Day Average  
- **INDEX-NDTW**: Nasdaq 100 Stocks Above 20-Day Average

## Usage

These indicators can be used with the standard OHLCV API:

```python
from tvkit.api.chart.ohlcv import OHLCV

async with OHLCV() as client:
    # Fetch historical breadth data
    bars = await client.get_historical_ohlcv('INDEX-NDTH', interval='1D', bars_count=5000)
    
    # Process breadth data for analysis
    latest_breadth = bars[-1].close  # Current percentage
    print(f"Current NASDAQ 100 breadth (200-day): {latest_breadth:.1f}%")
```

## Analysis Applications

These indicators are widely used for:

- **Quantitative liquidity models**: Measure market participation and liquidity conditions
- **Macro regime detection**: Identify bull/bear markets and trend changes  
- **Systematic trading strategies**: Generate signals based on market breadth
- **Risk management**: Assess market health and momentum

## Interpretation

- **> 70%**: Strong bullish breadth, broad market participation
- **50-70%**: Moderate bullish conditions
- **30-50%**: Neutral/mixed market conditions
- **< 30%**: Weak breadth, potential bearish conditions

## Example Analysis

```python
async def breadth_analysis():
    async with OHLCV() as client:
        # Get all three timeframes
        ndth = await client.get_historical_ohlcv('INDEX-NDTH', '1D', 100)  # 200-day
        ndfi = await client.get_historical_ohlcv('INDEX-NDFI', '1D', 100)  # 50-day
        ndtw = await client.get_historical_ohlcv('INDEX-NDTW', '1D', 100)  # 20-day
        
        # Current breadth levels
        current_200d = ndth[-1].close
        current_50d = ndfi[-1].close  
        current_20d = ndtw[-1].close
        
        print(f"Breadth Analysis:")
        print(f"  200-day: {current_200d:.1f}%")
        print(f"  50-day:  {current_50d:.1f}%")
        print(f"  20-day:  {current_20d:.1f}%")
        
        # Regime detection
        if current_200d > 60 and current_50d > 70:
            regime = "Bull Market"
        elif current_200d < 40 and current_50d < 30:
            regime = "Bear Market"
        else:
            regime = "Mixed/Transitional"
            
        print(f"  Market Regime: {regime}")
```

See `examples/breadth_indicators_example.py` for a comprehensive demonstration.