import requests

def get_travel_destinations(api_key):
    url = f"https://api.example.com/destinations?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_accommodation_options(destination, api_key):
    url = f"https://api.example.com/accommodations?destination={destination}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_travel_tips(destination, api_key):
    url = f"https://api.example.com/travel_tips?destination={destination}&api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None