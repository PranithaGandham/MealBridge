from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,Donee,Restaurant,FoodDonation,Notification
from .serializers import UserSerializer,DoneeSerializer,RestaurantSerializer,FoodDonationSerializer,NotificationSerializer
from .utils.send_email import send_donation_email,send_confirmation_email
from django.utils.timezone import now


class UserListView(generics.ListAPIView):
    """Retrieve a list of all users (Admin only)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserDetailView(generics.RetrieveAPIView):
    """Retrieve a single user by ID"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(APIView):
    """Register a new user"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    """Login an existing user"""

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid credentials'}, status=400)

class DoneeListView(generics.ListAPIView):
    """Retrieve a list of all donees (Admin only)"""
    queryset = Donee.objects.all()
    serializer_class = DoneeSerializer
    permission_classes = [permissions.IsAdminUser]

class DoneeDetailView(generics.RetrieveAPIView):
    """Retrieve a single donee by ID"""
    queryset = Donee.objects.all()
    serializer_class = DoneeSerializer
    permission_classes = [permissions.IsAuthenticated]

class DoneeCreateView(generics.CreateAPIView):
    """Create a new Donee profile (For NGOs)"""
    serializer_class = DoneeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ApproveDoneeView(APIView):
    """Manually approve a Donee (Admin only)"""
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, donee_id):
        try:
            donee = Donee.objects.get(id=donee_id)
            donee.is_approved = True
            donee.save()
            return Response({'message': 'Donee approved successfully'})
        except Donee.DoesNotExist:
            return Response({'error': 'Donee not found'}, status=404)
        
class RestaurantListView(generics.ListAPIView):
    """Retrieve all restaurants (Admin only)"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAdminUser]

class RestaurantDetailView(generics.RetrieveAPIView):
    """Retrieve a single restaurant by ID"""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

class RestaurantCreateView(generics.CreateAPIView):
    """Register a restaurant"""
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FoodDonationListView(generics.ListAPIView):
    """Retrieve all food donations"""
    queryset = FoodDonation.objects.all()
    serializer_class = FoodDonationSerializer
    permission_classes = [permissions.IsAuthenticated]

class FoodDonationDetailView(generics.RetrieveAPIView):
    """Retrieve a specific food donation"""
    queryset = FoodDonation.objects.all()
    serializer_class = FoodDonationSerializer
    permission_classes = [permissions.IsAuthenticated]


class FoodDonationCreateView(generics.CreateAPIView):
    """Create a new food donation (Only restaurants)"""
    serializer_class = FoodDonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        donation = serializer.save(restaurant=self.request.user.restaurant_profile, created_at=now())

        # Notify selected NGOs via email
        donees = donation.preferred_organizations.all()
        recipient_emails = [donee.user.email for donee in donees if donee.user.email]

        if recipient_emails:
            send_donation_email(recipient_emails, donation)


class FoodDonationClaimView(generics.UpdateAPIView):
    """NGOs can claim a donation"""
    queryset = FoodDonation.objects.all()
    serializer_class = FoodDonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.instance
        if not instance.is_claimed:
            instance.is_claimed = True
            instance.save()

            # Notify the restaurant via email
            send_confirmation_email(instance.restaurant.user.email, self.request.user.donee_profile.organization_name, instance)

class NotificationListView(generics.ListAPIView):
    """List all notifications for the logged-in user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-timestamp')

class NotificationDetailView(generics.RetrieveAPIView):
    """Retrieve a specific notification"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

class MarkNotificationReadView(generics.UpdateAPIView):
    """Mark a notification as read"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.instance.is_read = True
        serializer.save()
