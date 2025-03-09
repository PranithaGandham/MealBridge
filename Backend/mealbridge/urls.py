from django.urls import path
from .views import UserListView, UserDetailView, RegisterView, LoginView,DoneeCreateView,DoneeDetailView,DoneeListView,ApproveDoneeView,RestaurantListView, RestaurantDetailView, RestaurantCreateView,FoodDonationListView, FoodDonationDetailView, FoodDonationCreateView, FoodDonationClaimView,NotificationListView, NotificationDetailView, MarkNotificationReadView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),  # Get all users (Admin only)
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Get a specific user
    path('users/register/', RegisterView.as_view(), name='user-register'),  # User registration
    path('users/login/', LoginView.as_view(), name='user-login'),  # User login

    path('donees/', DoneeListView.as_view(), name='donee-list'),  # Get all donees (Admin only)
    path('donees/<int:pk>/', DoneeDetailView.as_view(), name='donee-detail'),  # Get specific donee
    path('donees/register/', DoneeCreateView.as_view(), name='donee-register'),  # Register as a donee
    path('donees/<int:donee_id>/approve/', ApproveDoneeView.as_view(), name='approve-donee'),  # Admin approves donee

    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),  # Get all restaurants (Admin only)
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),  # Get specific restaurant
    path('restaurants/register/', RestaurantCreateView.as_view(), name='restaurant-register'),  # Register a restaurant

    path('donations/', FoodDonationListView.as_view(), name='donation-list'),  # List all food donations
    path('donations/<int:pk>/', FoodDonationDetailView.as_view(), name='donation-detail'),  # Get specific donation
    path('donations/create/', FoodDonationCreateView.as_view(), name='donation-create'),  # Create a food donation
    path('donations/<int:pk>/claim/', FoodDonationClaimView.as_view(), name='donation-claim'),  # Claim a food donation

    path('notifications/', NotificationListView.as_view(), name='notification-list'),  # Get all notifications
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),  # Get specific notification
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='notification-read'),  # Mark notification as read
]