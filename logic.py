# logic.py
import yfinance as yf
import pandas_ta as ta
import pandas as pd

def get_signal(ticker):
    # 1. Fetch Data
    # We allow MultiIndex for now, we will flatten it manually below
    df = yf.download(ticker, period="1y", interval="1d", progress=False)
    
    if len(df) < 20: 
        return None

    # --- FIX 1: Flatten MultiIndex Columns (Handle yfinance update) ---
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    # ------------------------------------------------------------------

    # 2. Calculate Indicators
    # RSI (Relative Strength Index)
    df.ta.rsi(length=14, append=True)
    
    # EMA (Exponential Moving Average)
    df.ta.ema(length=200, append=True)
    
    # ATR (Average True Range)
    df.ta.atr(length=14, append=True)

    # --- FIX 2: Safer Bollinger Bands Calculation ---
    # Instead of append=True, we capture the result in a variable
    bbands = df.ta.bbands(length=20, sd=2)
    
    # Join it back to the main dataframe
    df = pd.concat([df, bbands], axis=1)
    
    # Dynamically find the column names (Starts with BBL for Lower, BBU for Upper)
    # This prevents the KeyError "BBL_20_2.0" vs "BBL_20_2"
    lower_band_col = [c for c in bbands.columns if c.startswith("BBL")][0]
    # ------------------------------------------------------------------

    # Get latest values
    last_row = df.iloc[-1]
    
    # Use .get() to avoid crashing if RSI/EMA are missing for some reason
    price = last_row.get('Close')
    rsi = last_row.get('RSI_14')
    ema_200 = last_row.get('EMA_200')
    atr = last_row.get('ATRr_14')
    
    # Use the dynamic column name we found earlier
    lower_band = last_row[lower_band_col]

    # Ensure we have all necessary data before proceeding
    if None in [price, rsi, ema_200, lower_band, atr]:
        return None

    # 3. Strategy Logic
    signal = "WAIT"
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0

    # Logic: Uptrend (Price > EMA) + Dip (RSI < 40)
    if price > ema_200 and rsi < 40:
        signal = "BUY"
        entry_price = round(lower_band, 2)
        stop_loss = round(entry_price - (2.0 * atr), 2)
        take_profit = round(entry_price + (3.0 * atr), 2)
    
    elif price < ema_200 and rsi > 70:
        signal = "SELL"

    return {
        "Ticker": ticker,
        "Price": round(price, 2),
        "Signal": signal,
        "Entry (Limit)": entry_price,
        "Stop Loss": stop_loss,
        "Take Profit": take_profit
    }