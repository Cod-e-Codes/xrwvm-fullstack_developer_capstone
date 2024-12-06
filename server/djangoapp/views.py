# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel  # Import the CarMake and CarModel models
from .restapis import get_request, analyze_review_sentiments


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body.decode("utf-8"))
            username = data.get('userName')
            password = data.get('password')

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
                logger.info(f"User {username} logged in successfully.")
            else:
                # Authentication failed
                response_data = {"userName": username, "status": "Authentication Failed"}
                logger.warning(f"Failed login attempt for username: {username}.")
        except json.JSONDecodeError:
            # Handle invalid JSON in request body
            response_data = {"status": "Error", "message": "Invalid JSON data"}
            logger.error("Invalid JSON data received for login.")
        except Exception as e:
            # Handle other exceptions
            response_data = {"status": "Error", "message": str(e)}
            logger.error(f"Error during login: {e}")
    else:
        # Respond to non-POST requests
        response_data = {"status": "Error", "message": "Invalid request method"}
        logger.warning("Invalid request method for login_user.")

    # Return the response as JSON
    return JsonResponse(response_data)

@csrf_exempt
def logout_request(request):
    """
    Handle logout requests. Logs out the current user and returns a JSON response.
    """
    if request.method == "POST":
        logout(request)  # Log out the user
        response_data = {"userName": "", "status": "Logged Out"}
        logger.info("User logged out successfully.")
    else:
        response_data = {"status": "Error", "message": "Invalid request method"}
        logger.warning("Invalid request method for logout_request.")

    return JsonResponse(response_data)


@csrf_exempt
def registration(request):
    """
    Handle user registration requests. Creates a new user and logs them in.
    """
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body.decode("utf-8"))
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                response_data = {"userName": username, "error": "Already Registered"}
                logger.warning(f"User {username} is already registered.")
            elif User.objects.filter(email=email).exists():
                response_data = {"email": email, "error": "Email Already Registered"}
                logger.warning(f"Email {email} is already registered.")
            else:
                # Create and save the new user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                # Log in the new user
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
                logger.info(f"User {username} registered and logged in successfully.")
        except json.JSONDecodeError:
            response_data = {"status": "Error", "message": "Invalid JSON data"}
            logger.error("Invalid JSON data received for registration.")
        except Exception as e:
            response_data = {"status": "Error", "message": str(e)}
            logger.error(f"Error during registration: {e}")
    else:
        response_data = {"status": "Error", "message": "Invalid request method"}
        logger.warning("Invalid request method for registration.")

    # Return the response as JSON
    return JsonResponse(response_data)


# Update the `get_dealerships` view
def get_dealerships(request, state="All"):
    """
    Get dealerships from the backend API.
    If a state is provided, fetch dealerships for that state only.
    """
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


# Add a `get_dealer_details` view
def get_dealer_details(request, dealer_id):
    """
    Get details of a specific dealer by dealer ID.
    """
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Add a `get_dealer_reviews` view
def get_dealer_reviews(request, dealer_id):
    """
    Get reviews for a specific dealer and analyze their sentiments.
    """
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail.get('review', ''))
            review_detail['sentiment'] = response.get('sentiment', 'unknown')
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

def get_cars(request):
    count = CarMake.objects.count()
    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})

@csrf_exempt
def add_review(request):
    """
    Handle a request to add a review. Only authenticated users can post reviews.

    Args:
        request: The Django request object.

    Returns:
        JsonResponse: JSON response indicating success or failure.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    if request.method == "POST":
        try:
            # Parse the request body into a dictionary
            data = json.loads(request.body.decode("utf-8"))

            # Call the post_review function with the data
            response = post_review(data)

            # Return the response from the backend
            return JsonResponse({"status": 200, "message": "Review added successfully", "response": response})
        except json.JSONDecodeError:
            return JsonResponse({"status": 400, "message": "Invalid JSON data"})
        except Exception as e:
            print(f"Error during review posting: {e}")
            return JsonResponse({"status": 500, "message": "Internal server error"})
    else:
        return JsonResponse({"status": 405, "message": "Method not allowed"})
