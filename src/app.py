import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from PIL import Image
import io
import matplotlib.pyplot as plt
import json
import time  # Add this import for retry logic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(page_title="Travel Buddy", layout="wide", page_icon="✈️")

# App title and description
st.title("✈️ Travel Buddy: Your AI Travel Assistant")
st.markdown("Plan your trip, convert currencies, and get AI-powered travel recommendations!")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Currency Exchange", "Destination Info", "AI Travel Assistant", "Language Translator", "Travel Budget Planner"])

# API keys (stored securely using environment variables)
import os
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# Functions for currency exchange
def get_exchange_rates(base_currency="USD"):
    """Get latest exchange rates"""
    try:
        url = f"https://open.er-api.com/v6/latest/{base_currency}"
        response = requests.get(url)
        data = response.json()
        if data["result"] == "success":
            return data["rates"]
        else:
            st.error("Failed to fetch exchange rates")
            return {}
    except Exception as e:
        st.error(f"Error fetching exchange rates: {e}")
        return {}

def get_historical_rates(base_currency, target_currency, days=7):
    """Get historical exchange rates for the past days"""
    rates = []
    dates = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        dates.append(date_str)
        
        try:
            url = f"https://open.er-api.com/v6/historical/{date_str}?base={base_currency}"
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                rates.append(data["rates"][target_currency])
            else:
                rates.append(None)
        except:
            rates.append(None)
    
    return list(reversed(dates)), list(reversed(rates))

# Function to get weather information
def get_weather(city):
    """Get current weather for a city"""
    if not WEATHER_API_KEY:
        st.error("Weather API key not configured. Please set WEATHER_API_KEY in your environment variables.")
        return None
        
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error fetching weather: {e}")
        return None

# Updated to use Mistral-7B model from Hugging Face instead of Gemma
def get_ai_recommendation(prompt):
    """Get travel recommendations from Mistral-7B model via Hugging Face"""
    if not HUGGINGFACE_API_KEY:
        st.warning("Hugging Face API key not configured. Using template responses.")
        return get_template_response(prompt)
        
    try:
        # Using Mistral-7B instead of Gemma for better accessibility
        API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        
        # Format prompt specifically for Mistral model
        formatted_prompt = f"""<s>[INST] You are a helpful travel assistant providing concise, practical travel advice.

{prompt} [/INST]"""
        
        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": 500,
                "do_sample": True,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.95,
                "return_full_text": False
            }
        }
        
        # Add retry logic for model loading
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()[0]["generated_text"]
                return result.strip()
                
            elif response.status_code == 503 and "loading" in response.text.lower():
                # Model is loading, wait and retry
                if attempt < max_retries - 1:
                    st.warning(f"Model is loading, retrying in {retry_delay} seconds... (Attempt {attempt+1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
            
            # Fall back to templates for any other error
            st.error(f"Error from Hugging Face API: {response.status_code}")
            return get_template_response(prompt)
    except Exception as e:
        st.error(f"Error getting AI recommendation: {e}")
        return get_template_response(prompt)

# Template response function for fallback
def get_template_response(prompt):
    """Fallback template responses when API fails"""
    prompt_lower = prompt.lower()
    
    # Check for common travel topics
    if any(word in prompt_lower for word in ["pack", "packing", "bring"]):
        return """Here are essential items to pack:
- Weather-appropriate clothing (layers recommended)
- Comfortable walking shoes
- Travel documents (passport, visas, tickets)
- Travel adapter and electronics chargers
- Basic toiletries and medications
- Travel insurance information
- Local currency or credit/debit cards"""
    
    elif any(word in prompt_lower for word in ["budget", "cheap", "affordable", "cost"]):
        return """Budget travel tips:
- Travel during shoulder season (between peak and off-season)
- Stay in hostels or use homestay services
- Use public transportation instead of taxis
- Cook some meals instead of eating out for every meal
- Look for free attractions and city walking tours
- Use flight comparison tools and set fare alerts"""
    
    elif any(word in prompt_lower for word in ["itinerary", "plan", "schedule", "day trip"]):
        return """Suggested itinerary structure:
- Day 1: Focus on main attractions and get oriented
- Day 2: Explore neighborhoods and local culture
- Day 3: Take a day trip to nearby attractions
- Balance your schedule with both planned activities and free time
- Research opening hours for key attractions
- Group activities by geographical proximity to save travel time"""
    
    # For city-specific information
    for city in ["paris", "london", "rome", "new york", "tokyo", "bangkok"]:
        if city in prompt_lower:
            return f"""Top things to do in {city.title()}:
- Visit the main historical sites and landmarks
- Try local cuisine at recommended restaurants
- Explore museums and cultural centers
- Experience the local markets
- Take a walking tour to learn about the city's history
- Enjoy the local parks and public spaces"""
    
    # Default response for other travel questions
    return """Travel recommendations:
- Research your destination thoroughly before traveling
- Learn a few basic phrases in the local language
- Respect local customs and traditions
- Stay flexible with your plans
- Connect with locals for authentic experiences
- Keep a travel journal to document your experiences
- Consider purchasing travel insurance for peace of mind"""

# Home page
if page == "Home":
    st.header("Welcome to Travel Buddy!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Travel Buddy** helps you:
        - Convert currencies with real-time exchange rates
        - Get information about travel destinations
        - Receive AI-powered travel recommendations
        - Translate languages for your journey
        - Plan and manage your travel budget
        
        Start by selecting an option from the sidebar!
        """)
    
    with col2:
        # Display a travel-related image
        st.image("https://images.unsplash.com/photo-1501785888041-af3ef285b470?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fHRyYXZlbHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60")

# Currency Exchange page
elif page == "Currency Exchange":
    st.header("Currency Exchange")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Currency Converter")
        rates = get_exchange_rates()
        if rates:
            currencies = list(rates.keys())
            
            from_currency = st.selectbox("From Currency", currencies, index=currencies.index("USD") if "USD" in currencies else 0)
            to_currency = st.selectbox("To Currency", currencies, index=currencies.index("EUR") if "EUR" in currencies else 0)
            
            # Update rates based on selected base currency
            if from_currency != "USD":
                rates = get_exchange_rates(from_currency)
            
            amount = st.number_input("Amount", min_value=0.01, value=100.0, step=10.0)
            
            if rates and to_currency in rates:
                converted_amount = amount * rates[to_currency]
                st.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
                
                # Show exchange rate
                st.info(f"1 {from_currency} = {rates[to_currency]:.4f} {to_currency}")
                st.info(f"1 {to_currency} = {(1/rates[to_currency]):.4f} {from_currency}")
    
    with col2:
        st.subheader("Historical Exchange Rate")
        if rates:
            base = st.selectbox("Base Currency", currencies, index=currencies.index("USD") if "USD" in currencies else 0, key="hist_base")
            target = st.selectbox("Target Currency", currencies, index=currencies.index("EUR") if "EUR" in currencies else 0, key="hist_target")
            days = st.slider("Number of days", min_value=7, max_value=30, value=7)
            
            dates, historical_rates = get_historical_rates(base, target, days)
            
            if all(rate is not None for rate in historical_rates):
                df = pd.DataFrame({
                    'Date': dates,
                    'Rate': historical_rates
                })
                
                fig = px.line(df, x='Date', y='Rate', title=f'{base}/{target} Exchange Rate History')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Some historical data is unavailable")

# Destination Info page
elif page == "Destination Info":
    st.header("Destination Information")
    
    city = st.text_input("Enter City Name")
    
    if city:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Weather in {city}")
            weather_data = get_weather(city)
            
            if weather_data and weather_data.get("cod") != "404":
                temp = weather_data["main"]["temp"]
                weather_desc = weather_data["weather"][0]["description"]
                humidity = weather_data["main"]["humidity"]
                wind_speed = weather_data["wind"]["speed"]
                
                st.markdown(f"**Temperature:** {temp}°C")
                st.markdown(f"**Conditions:** {weather_desc.title()}")
                st.markdown(f"**Humidity:** {humidity}%")
                st.markdown(f"**Wind Speed:** {wind_speed} m/s")
            else:
                st.error("City not found or weather data unavailable")
        
        with col2:
            st.subheader(f"About {city}")
            
            # Generate city information using AI
            city_info_prompt = f"Provide a brief overview of {city} as a travel destination in 3-4 sentences."
            city_info = get_ai_recommendation(city_info_prompt)
            st.write(city_info)
            
            # What to do there
            things_to_do_prompt = f"List 5 top attractions or things to do in {city} in bullet point format."
            things_to_do = get_ai_recommendation(things_to_do_prompt)
            st.subheader("Top Attractions")
            st.write(things_to_do)

# AI Travel Assistant page
elif page == "AI Travel Assistant":
    st.header("AI Travel Assistant")
    
    st.markdown("""
    Ask our AI assistant for personalized travel advice, recommendations, or information.
    Examples:
    - "What should I pack for a winter trip to Norway?"
    - "Suggest a 3-day itinerary for Rome"
    - "What are some budget-friendly destinations in Southeast Asia?"
    """)
    
    user_query = st.text_area("Your travel question", height=100)
    
    if st.button("Get AI Recommendation"):
        if user_query:
            with st.spinner("Generating recommendation..."):
                recommendation = get_ai_recommendation(user_query)
                st.markdown("### AI Recommendation")
                st.write(recommendation)
        else:
            st.warning("Please enter a question for the AI assistant")

# Language Translator page
elif page == "Language Translator":
    st.header("Language Translator")
    
    languages = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Chinese", "Russian", "Arabic"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox("From Language", languages)
    
    with col2:
        target_lang = st.selectbox("To Language", languages, index=1)
    
    text_to_translate = st.text_area("Enter text to translate", height=150)
    
    if st.button("Translate") and text_to_translate:
        with st.spinner("Translating..."):
            try:
                prompt = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text_to_translate}"
                translated_text = get_ai_recommendation(prompt)
                
                st.markdown("### Translation")
                st.write(translated_text)
                
                # Provide some travel-related phrases
                if len(text_to_translate) < 100:  # Only for shorter texts
                    st.markdown("### Additional Useful Phrases")
                    phrases_prompt = f"Provide 3 additional useful related travel phrases in {target_lang} with their {source_lang} translations. Format as a bullet list."
                    phrases = get_ai_recommendation(phrases_prompt)
                    st.write(phrases)
            except Exception as e:
                st.error(f"Translation error: {e}")

# Travel Budget Planner page
elif page == "Travel Budget Planner":
    st.header("Travel Budget Planner")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trip Details")
        destination = st.text_input("Destination")
        duration = st.number_input("Duration (days)", min_value=1, max_value=90, value=7)
        travelers = st.number_input("Number of Travelers", min_value=1, max_value=10, value=2)
        budget_category = st.selectbox("Budget Category", ["Budget", "Moderate", "Luxury"])
    
    with col2:
        if destination:
            st.subheader("AI Budget Recommendation")
            budget_prompt = f"Create a detailed travel budget for {travelers} travelers going to {destination} for {duration} days with a {budget_category.lower()} budget. Include estimated costs for accommodation, food, transportation, activities, and miscellaneous expenses. Format as bullet points with a total at the end."
            
            with st.spinner("Generating budget recommendation..."):
                budget_recommendation = get_ai_recommendation(budget_prompt)
                st.write(budget_recommendation)
    
    # Custom budget planner
    st.subheader("Custom Budget Planner")
    
    # Initialize budget categories in session state if not already there
    if 'budget_items' not in st.session_state:
        st.session_state.budget_items = {
            'Accommodation': 0.0,
            'Food': 0.0,
            'Transportation': 0.0,
            'Activities': 0.0,
            'Shopping': 0.0,
            'Miscellaneous': 0.0
        }
    
    # Display budget inputs
    col1, col2 = st.columns(2)
    
    with col1:
        for item in list(st.session_state.budget_items.keys())[:3]:
            st.session_state.budget_items[item] = st.number_input(
                f"{item} budget ({destination})", 
                min_value=0.0, 
                value=float(st.session_state.budget_items[item]),
                key=f"budget_{item}"
            )
    
    with col2:
        for item in list(st.session_state.budget_items.keys())[3:]:
            st.session_state.budget_items[item] = st.number_input(
                f"{item} budget ({destination})", 
                min_value=0.0, 
                value=float(st.session_state.budget_items[item]),
                key=f"budget_{item}"
            )
    
    # Calculate and display total budget
    total_budget = sum(st.session_state.budget_items.values())
    st.subheader(f"Total Budget: ${total_budget:.2f}")
    
    # Create a pie chart for budget distribution
    if total_budget > 0:
        fig, ax = plt.subplots(figsize=(8, 6))
        labels = st.session_state.budget_items.keys()
        sizes = st.session_state.budget_items.values()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
        
        # Per day and per person calculations
        st.markdown(f"**Budget per day:** ${total_budget/duration:.2f}")
        st.markdown(f"**Budget per person:** ${total_budget/travelers:.2f}")
        st.markdown(f"**Budget per person per day:** ${total_budget/(travelers*duration):.2f}")

# Footer
st.markdown("---")
st.markdown("© 2025 Travel Buddy | Created with Streamlit")