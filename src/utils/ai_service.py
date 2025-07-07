from transformers import pipeline

def get_travel_recommendations(destination, interests):
    # Load the AI model for generating recommendations
    recommendation_model = pipeline("text-generation", model="gpt-3.5-turbo")

    # Create a prompt for the AI model
    prompt = f"Suggest a travel itinerary for someone visiting {destination} who is interested in {', '.join(interests)}."

    # Generate recommendations
    recommendations = recommendation_model(prompt, max_length=200, num_return_sequences=1)

    return recommendations[0]['generated_text']

def answer_travel_query(query):
    # Load the AI model for answering questions
    qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

    # Define a context for the model to answer questions
    context = "Traveling can be an exciting experience. You can explore new cultures, try different cuisines, and enjoy various activities. Always check travel advisories and local regulations before planning your trip."

    # Get the answer to the user's query
    answer = qa_model(question=query, context=context)

    return answer['answer']