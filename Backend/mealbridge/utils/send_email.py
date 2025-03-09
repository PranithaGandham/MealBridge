from django.core.mail import send_mail

def send_donation_email(recipients, donation):
    """Send email notification to selected Donees when a new food donation is posted."""
    subject = "New Food Donation Available 🍽️"
    message = f"""
    Hello,

    A new food donation is available from {donation.restaurant.restaurant_name}.

    📍 Location: {donation.restaurant.location}
    🍽️ Food Details: {donation.food_details}
    🕒 Expiry Time: {donation.expiry_time.strftime('%Y-%m-%d %H:%M')}

    If interested, please claim it via the MealBridge platform.

    Best Regards,
    MealBridge Team
    """
    send_mail(subject, message, 'your-email@gmail.com', recipients, fail_silently=False)

def send_confirmation_email(restaurant_email, ngo_name, donation):
    """Send email to restaurant when an NGO accepts a donation."""
    subject = "Your Food Donation Has Been Claimed ✅"
    message = f"""
    Hello {donation.restaurant.owner_name},

    Your food donation has been successfully claimed by {ngo_name}.

    🍽️ Food Details: {donation.food_details}
    🕒 Expiry Time: {donation.expiry_time.strftime('%Y-%m-%d %H:%M')}

    Thank you for contributing to the community!

    Best Regards,
    MealBridge Team
    """
    send_mail(subject, message, 'your-email@gmail.com', [restaurant_email], fail_silently=False)
