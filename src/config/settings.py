import os

class Config:
    """Configuration settings for the travel currency application."""
    
    # API Keys
    CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY")
    TRAVEL_API_KEY = os.getenv("TRAVEL_API_KEY")
    AI_SERVICE_API_KEY = os.getenv("AI_SERVICE_API_KEY")

    # Application settings
    DEBUG = os.getenv("DEBUG", "False") == "True"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    # Other settings
    DEFAULT_CURRENCY = "USD"
    SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"]
    DEFAULT_DESTINATION = "Paris"