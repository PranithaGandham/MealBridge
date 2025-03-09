from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User,Donee,Restaurant,FoodDonation,Notification

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'is_verified', 'profile_picture', 'phone_number', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Hash the password before saving"""
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
class DoneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donee
        fields = '__all__'
        read_only_fields = ['is_approved']

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class FoodDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDonation
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'