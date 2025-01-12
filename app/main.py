import streamlit as st
from utils import load_config
from stock_handler import fetch_stock_data, get_stock_summary

def main():
    load_config()

    st.title("Stock Data Summarizer")
    st.write("Enter a stock ticker symbol to retrieve its stock price, analyst recommendations, and fundamentals.")

    stock_symbol = st.text_input("Enter Stock Symbol (e.g., NVDA)", "")
    
    if st.button("Fetch Data"):
        if not stock_symbol:
            st.error("Please provide a stock symbol.")
        else:
            stock_data = fetch_stock_data(stock_symbol)
            if "error" in stock_data:
                st.error(stock_data["error"])
            else:
                summary = get_stock_summary(stock_data, stock_symbol)
                st.subheader("Stock Summary")
                st.markdown(summary)

if __name__ == "__main__":
    main()
