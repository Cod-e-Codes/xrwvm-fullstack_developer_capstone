from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login/', view=views.login_user, name='login'),
    path('logout/', view=views.logout_request, name='logout'),
    path('register/', view=views.registration, name='register'),
    path('get_cars/', view=views.get_cars, name='get_cars'),
    path('get_dealerships/', view=views.get_dealerships, name='get_dealerships'),
    path('get_dealerships/<str:state>/', view=views.get_dealerships, name='get_dealerships_by_state'),
    path('dealer/<int:dealer_id>/', view=views.get_dealer_details, name='dealer_details'),
    path('reviews/dealer/<int:dealer_id>/', view=views.get_dealer_reviews, name='get_dealer_reviews'),
    path('add_review/', view=views.add_review, name='add_review'),
]