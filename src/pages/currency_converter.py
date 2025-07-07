import streamlit as st
from utils.currency_api import get_exchange_rate

def currency_converter():
    st.title("Currency Converter")
    
    # Input for the amount to convert
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    
    # Input for the currency to convert from
    from_currency = st.selectbox("From Currency", ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"])
    
    # Input for the currency to convert to
    to_currency = st.selectbox("To Currency", ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"])
    
    if st.button("Convert"):
        if amount > 0:
            exchange_rate = get_exchange_rate(from_currency, to_currency)
            converted_amount = amount * exchange_rate
            st.success(f"{amount} {from_currency} is equal to {converted_amount:.2f} {to_currency}")
        else:
            st.error("Please enter a valid amount.")

if __name__ == "__main__":
    currency_converter()