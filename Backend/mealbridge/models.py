from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('restaurant_owner', 'Restaurant Owner'),
        ('donee', 'Donee'),
    ]

    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'phone_number']

    def __str__(self):
        return f"{self.email} - {self.role}"

# Donee Model

class Donee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="donee_profile")
    organization_name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    location = models.TextField()
    registration_certificate = models.FileField(upload_to='registration_certificates/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)  # Admin manually verifies NGOs
    previous_donations_received = models.ManyToManyField('FoodDonation', blank=True, related_name="received_by")

    def __str__(self):
        return self.organization_name
    
# Restaurant Model
    
class Restaurant(models.Model):
    CUISINE_CHOICES = [
        ('Indian', 'Indian'),
        ('Chinese', 'Chinese'),
        ('Italian', 'Italian'),
        ('Mexican', 'Mexican'),
        ('Continental', 'Continental'),
        ('Others', 'Others'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="restaurant_profile")
    restaurant_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    location = models.TextField()
    cuisine_type = models.CharField(max_length=20, choices=CUISINE_CHOICES, default='Indian')
    restaurant_logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    food_donations = models.ManyToManyField('FoodDonation', blank=True, related_name="donated_by")

    def __str__(self):
        return self.restaurant_name
    
#Food Donation Model

class FoodDonation(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='donations')
    food_details = models.TextField()
    quantity = models.PositiveIntegerField()
    expiry_time = models.DateTimeField()
    preferred_organizations = models.ManyToManyField('Donee', blank=True, related_name='preferred_food')
    is_claimed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)

    def __str__(self):
        return f"Donation from {self.restaurant.restaurant_name} - {self.food_details[:20]}"

    def is_expired(self):
        """Check if the food donation has expired."""
        return timezone.now() > self.expiry_time

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message[:30]}"