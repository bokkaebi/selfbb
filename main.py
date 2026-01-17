# main.py
import streamlit as st
import pandas as pd
from tickers import WATCHLIST
from logic import get_signal

# Mobile optimization: Set page to wide, though mobile handles this automatically
st.set_page_config(page_title="My Stock Picker", layout="centered")

st.title("📈 Daily Signals")
st.write("Moomoo Strategy Screener")

# 1. The Summary Table (The "At a Glance" view)
st.subheader("Today's Opportunities")

results = []
# Show a progress bar because processing 20 stocks takes time
progress_bar = st.progress(0)

for i, ticker in enumerate(WATCHLIST):
    data = get_signal(ticker)
    if data and data['Signal'] == "BUY":
        results.append(data)
    progress_bar.progress((i + 1) / len(WATCHLIST))

progress_bar.empty() # Hide bar when done

if not results:
    st.info("No BUY signals today. Relax! 😴")
else:
    # Display each opportunity as a "Card" for mobile readability
    for item in results:
        with st.container():
            st.markdown(f"### {item['Ticker']}")
            
            # Use columns for mobile layout (Side by Side metrics)
            col1, col2, col3 = st.columns(3)
            col1.metric("Action", item['Signal'], delta="Ready")
            col2.metric("Limit Price", f"${item['Entry (Limit)']}")
            col3.metric("Current", f"${item['Price']}")
            
            # The Trading Plan
            st.warning(f"📉 **Stop Loss:** ${item['Stop Loss']}")
            st.success(f"🎯 **Take Profit:** ${item['Take Profit']}")
            
            # Copy Helper for Moomoo
            # Creates a string you can copy-paste into notes
            order_string = f"Limit Buy {item['Ticker']} @ {item['Entry (Limit)']}, SL {item['Stop Loss']}"
            st.code(order_string, language="text")
            
            st.divider()

# 2. Deep Dive (Optional)
st.subheader("Research")
selected_ticker = st.selectbox("Select Asset to view Chart", WATCHLIST)
# You can add a simple Plotly chart here later