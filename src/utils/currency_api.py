import requests
import os

def get_exchange_rate(base_currency, target_currency):
    api_key = os.getenv('CURRENCY_API_KEY')
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if target_currency in data['rates']:
            return data['rates'][target_currency]
        else:
            raise ValueError(f"Target currency '{target_currency}' not found.")
    else:
        raise Exception("Error fetching exchange rates.")

def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    return amount * exchange_rate