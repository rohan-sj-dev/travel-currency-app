# Travel Buddy - AI Travel Assistant

A comprehensive travel planning application built with Streamlit that provides currency conversion, weather information, AI-powered travel recommendations, language translation, and budget planning.

## Features

- **Currency Exchange**: Real-time currency conversion with historical rate charts
- **Destination Info**: Weather information and AI-generated city guides
- **AI Travel Assistant**: Personalized travel recommendations using Mistral-7B
- **Language Translator**: AI-powered text translation
- **Travel Budget Planner**: Interactive budget planning with visualizations

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/rohan-sj-dev/travel-currency-app.git
cd travel-currency-app
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory and add your API keys:
```
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
EXCHANGERATE_API_KEY=your_exchange_rate_api_key_here
WEATHER_API_KEY=your_openweather_api_key_here
```

### 4. Run the application
```bash
streamlit run src/app.py
```

## API Keys Required

1. **Hugging Face API Key**: Get it from [Hugging Face](https://huggingface.co/settings/tokens)
2. **Exchange Rate API Key**: Get it from [ExchangeRate-API](https://www.exchangerate-api.com/)
3. **Weather API Key**: Get it from [OpenWeatherMap](https://openweathermap.org/api)

## Project Structure

```
travel-currency-app/
├── src/
│   └── app.py              # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Security Note

Never commit API keys to version control. Always use environment variables or `.env` files that are excluded from git tracking.
│   │   ├── currency_api.py       # Functions to interact with currency exchange API
│   │   ├── travel_api.py         # Functions to interact with travel-related API
│   │   └── ai_service.py         # Functions for AI model interactions
│   ├── models
│   │   └── recommendation_model.py # Recommendation model for AI assistant
│   └── config
│       └── settings.py           # Configuration settings for the application
├── data
│   └── country_info.json         # JSON data with country information
├── requirements.txt              # List of dependencies for the project
├── .env.example                   # Template for environment variables
├── .gitignore                     # Files and directories to ignore by Git
└── README.md                      # Documentation for the project
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/travel-currency-app.git
   ```
2. Navigate to the project directory:
   ```
   cd travel-currency-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Set up your environment variables by creating a `.env` file based on the `.env.example` template.
2. Run the application:
   ```
   streamlit run src/app.py
   ```
3. Open your web browser and go to `http://localhost:8501` to access the app.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.
