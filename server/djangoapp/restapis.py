# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set backend URL and sentiment analyzer URL from environment variables
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    """
    Perform a GET request to the backend API.
    
    Args:
        endpoint (str): The specific endpoint of the backend API.
        **kwargs: Keyword arguments representing query parameters.
        
    Returns:
        dict: The JSON response from the backend API.
    """
    # Build the query string
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    # Construct the request URL
    request_url = f"{backend_url}/{endpoint}?{params}"
    print(f"GET from {request_url}")  # Debug log for the request URL

    try:
        # Perform the GET request
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        # Log the error and return an error message
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}


def analyze_review_sentiments(text):
    """
    Consume the sentiment analysis microservice to analyze sentiments of a given text.

    Args:
        text (str): The text to analyze.

    Returns:
        dict: The JSON response from the sentiment analysis microservice.
    """
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        # Call the GET method of requests library with the URL
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except Exception as err:
        print(f"Unexpected error occurred: {err}")
        print("Network exception occurred")
        return {"error": "Network exception occurred"}

def post_review(data_dict):
    """
    Post a review to the backend API.

    Args:
        data_dict (dict): Dictionary containing the review data.

    Returns:
        dict: The JSON response from the backend API.
    """
    request_url = f"{backend_url}/insert_review"
    print(f"POST to {request_url} with data: {data_dict}")  # Debug log

    try:
        # Perform the POST request
        response = requests.post(request_url, json=data_dict)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        # Log the error and return an error message
        print(f"Network exception occurred: {e}")
        return {"error": "Network exception occurred"}
