from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path(route='login/', view=views.login_user, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),
    path(route='register/', view=views.registration, name='register'),  # Registration path
    path(route='get_cars/', view=views.get_cars, name='get_cars'),       # Get cars path
    path(route='get_dealerships/', view=views.get_dealerships, name='get_dealerships'),  # Get dealerships
    path(route='get_dealer_reviews/<int:dealer_id>/', view=views.get_dealer_reviews, name='get_dealer_reviews'),  # Get dealer reviews
    path(route='add_review/', view=views.add_review, name='add_review'),  # Add review
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
