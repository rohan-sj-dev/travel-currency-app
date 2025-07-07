from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

class RecommendationModel:
    def __init__(self, data):
        self.data = data
        self.model = NearestNeighbors(n_neighbors=5, algorithm='auto')
        self.model.fit(self.data[['latitude', 'longitude']])

    def get_recommendations(self, user_location, num_recommendations=5):
        distances, indices = self.model.kneighbors([user_location])
        recommended_destinations = self.data.iloc[indices[0]]
        return recommended_destinations

def load_country_data(file_path):
    country_data = pd.read_json(file_path)
    return country_data

def main():
    country_data = load_country_data('../data/country_info.json')
    recommendation_model = RecommendationModel(country_data)
    user_location = [37.7749, -122.4194]  # Example: San Francisco coordinates
    recommendations = recommendation_model.get_recommendations(user_location)
    print(recommendations)

if __name__ == "__main__":
    main()