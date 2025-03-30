from django.urls import path
from travel.views import register_user, user_detail, login_user, travel_request_list, travel_request_detail,all_travel_requests

urlpatterns = [
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('api/user/', user_detail, name='user_detail'),
    path('api/travel-requests/', travel_request_list, name='travel_request_list'),
    path('api/travel-requests/<int:pk>/', travel_request_detail, name='travel_request_detail'),
    path('api/all-travel-requests/', all_travel_requests, name='all_travel_requests'),
]
