import streamlit as st
from utils.travel_api import get_destination_suggestions, create_itinerary
from utils.currency_api import get_currency_rates

def travel_planner():
    st.title("Travel Planner")
    
    # Destination Suggestions
    st.header("Destination Suggestions")
    destinations = get_destination_suggestions()
    selected_destination = st.selectbox("Choose a destination:", destinations)
    
    if selected_destination:
        st.write(f"You have selected: {selected_destination}")
        
        # Itinerary Creation
        st.header("Create Your Itinerary")
        itinerary_items = st.text_area("List your itinerary items (one per line):")
        
        if st.button("Create Itinerary"):
            itinerary = create_itinerary(itinerary_items.splitlines())
            st.write("Your Itinerary:")
            st.write(itinerary)
    
    # Currency Information
    st.header("Currency Information")
    currency = st.selectbox("Select currency for your destination:", ["USD", "EUR", "GBP", "JPY"])
    
    if currency:
        rates = get_currency_rates(currency)
        st.write(f"Current exchange rates for {currency}:")
        st.write(rates)

if __name__ == "__main__":
    travel_planner()