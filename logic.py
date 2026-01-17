# logic.py
import yfinance as yf
import pandas_ta as ta

def get_signal(ticker):
    # 1. Fetch Data (1 Year of Daily Data)
    df = yf.download(ticker, period="1y", interval="1d", progress=False)
    
    if len(df) < 20: return None # Not enough data

    # 2. Calculate Indicators
    # RSI for Overbought/Oversold
    df.ta.rsi(length=14, append=True)
    # EMA 200 for Trend Direction
    df.ta.ema(length=200, append=True)
    # Bollinger Bands for volatility entries
    df.ta.bbands(length=20, sd=2, append=True)
    # ATR for Stop Loss calculation
    df.ta.atr(length=14, append=True)

    # Get latest values (handling multi-level columns if necessary)
    last_row = df.iloc[-1]
    price = last_row['Close']
    rsi = last_row['RSI_14']
    ema_200 = last_row['EMA_200']
    lower_band = last_row['BBL_20_2.0']
    atr = last_row['ATRr_14']

    # 3. Strategy Logic (Example: Pullback Strategy)
    # Buy if: Trend is UP (Price > EMA200) AND Stock is dipping (RSI < 40)
    
    signal = "WAIT"
    entry_price = 0.0
    stop_loss = 0.0
    take_profit = 0.0

    if price > ema_200 and rsi < 40:
        signal = "BUY"
        # LOGIC: Don't buy at market. Place Limit at the Bollinger Lower Band
        # This catches the 'wick' of the candle.
        entry_price = round(lower_band, 2)
        
        # LOGIC: Stop Loss is 2x Volatility away
        stop_loss = round(entry_price - (2.0 * atr), 2)
        
        # LOGIC: Take Profit is 3x Volatility up
        take_profit = round(entry_price + (3.0 * atr), 2)
    
    elif price < ema_200 and rsi > 70:
        signal = "SELL" # Or "Take Profit" if you own it

    return {
        "Ticker": ticker,
        "Price": round(price, 2),
        "Signal": signal,
        "Entry (Limit)": entry_price,
        "Stop Loss": stop_loss,
        "Take Profit": take_profit
    }