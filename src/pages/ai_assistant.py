from streamlit import st
from utils.ai_service import get_travel_recommendations, answer_query

def ai_assistant():
    st.title("AI Travel Assistant")
    
    st.write("Welcome to the AI Travel Assistant! Ask me anything about your travel plans.")
    
    user_query = st.text_input("What would you like to know?")
    
    if st.button("Get Answer"):
        if user_query:
            answer = answer_query(user_query)
            st.write(answer)
        else:
            st.write("Please enter a query.")
    
    st.write("Or, get personalized travel recommendations based on your preferences.")
    
    destination = st.text_input("Enter your preferred destination:")
    travel_type = st.selectbox("Select the type of travel:", ["Leisure", "Business", "Adventure", "Cultural"])
    
    if st.button("Get Recommendations"):
        if destination:
            recommendations = get_travel_recommendations(destination, travel_type)
            st.write("Here are some recommendations for you:")
            for rec in recommendations:
                st.write(f"- {rec}")
        else:
            st.write("Please enter a destination.") 

if __name__ == "__main__":
    ai_assistant()