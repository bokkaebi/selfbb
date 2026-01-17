# main_local.py
import time
from tickers import WATCHLIST
from logic import get_signal

def run_analysis():
    print(f"\n{'='*40}")
    print(f"🚀 STARTING LOCAL ANALYSIS ({len(WATCHLIST)} Tickers)")
    print(f"{'='*40}\n")

    found_opportunities = 0

    for ticker in WATCHLIST:
        print(f"🔎 Scanning {ticker:<10} ... ", end="", flush=True)
        
        try:
            # Call the shared logic function
            data = get_signal(ticker)
            
            if data is None:
                print("⚠️  (Not enough data/Error)")
                continue

            # Check Signal type
            signal = data['Signal']
            price = data['Price']

            if signal == "BUY":
                print("✅  BUY SIGNAL!")
                print(f"   -----------------------------------")
                print(f"   💰 Current Price: ${price}")
                print(f"   📉 Limit Entry:   ${data['Entry (Limit)']}")
                print(f"   🛑 Stop Loss:     ${data['Stop Loss']}")
                print(f"   🎯 Take Profit:   ${data['Take Profit']}")
                print(f"   📝 Moomoo Note:   Limit Buy {ticker} @ {data['Entry (Limit)']}")
                print(f"   -----------------------------------")
                found_opportunities += 1
            
            elif signal == "SELL":
                print(f"🔻 SELL (Overbought - Price: ${price})")
            
            else:
                print(f"💤 WAIT (Neutral - Price: ${price})")
        
        except Exception as e:
            print(f"❌ CRASH: {e}")

    print(f"\n{'='*40}")
    print(f"✨ DONE. Found {found_opportunities} Buy Signals.")
    print(f"{'='*40}")

if __name__ == "__main__":
    run_analysis()