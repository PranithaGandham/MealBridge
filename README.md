# MealBridge

MealBridge is a web application designed to connect restaurants with NGOs and charitable organizations to facilitate food donations. The platform allows restaurants to post surplus food donations, and NGOs can claim them based on their needs.

![Alt text](https://github.com/PranithaGandham/MealBridge/blob/main/Screenshot%202025-03-08%20195033.png)

## Features

### For Restaurants:
- Register and manage profile details
- Post food donations with images, quantity, expiry time, and preferred NGOs
- Receive email notifications when an NGO claims a donation

### For NGOs (Donees):
- Register and manage organization details
- View available food donations and claim them
- Receive email notifications when a new donation is posted

### General Features:
- Secure authentication using Django authentication
- Admin approval for NGO registrations
- Email notifications for donation updates
- User-friendly API with Django REST Framework

![Alt text](https://github.com/PranithaGandham/MealBridge/blob/main/Screenshots/Screenshot%202025-03-08%20195349.png)


## Models

### 1. **Donee (NGOs/Charitable Organizations)**
- `user`: One-to-One relation with User
- `organization_name`
- `contact_person_name`
- `phone_number`
- `location`
- `registration_certificate`: File Upload
- `is_approved`: Boolean (Manually set True after verification)
- `previous_donations_received`: ManyToMany relation with FoodDonation
- **Features**: Profile image for NGO, list of received donations

### 2. **Restaurant**
- `user`: One-to-One relation with User
- `restaurant_name`
- `owner_name`
- `phone_number`
- `location`
- `cuisine_type`: ChoiceField (Indian, Chinese, Italian, etc.)
- `restaurant_logo`: ImageField (optional)
- `food_donations`: Related to FoodDonation

### 3. **Food Donation**
- `restaurant`: ForeignKey to Restaurant
- `food_details`: TextField for description
- `quantity`
- `expiry_time`: DateTimeField
- `preferred_organizations`: ManyToManyField with Donee
- `is_claimed`: Boolean (default: False)
- `created_at`: Auto timestamp
- `image`: ImageField (optional)
- **Features**: Store images, track which NGO accepts the donation

### 4. **Notifications**
- `user`: ForeignKey to User (recipient)
- `message`
- `is_read`: Boolean (default: False)
- `timestamp`: Auto timestamp
- **Functionality**:
  - NGOs receive notifications when a restaurant posts a donation
  - Restaurants receive notifications when an NGO claims the donation

## Email Notifications
- **Donees receive emails** when a restaurant submits a donation.
- **Restaurants receive confirmation emails** when an NGO claims a donation.
- Implemented using Django's Email module with SMTP settings.

![Alt text](https://github.com/PranithaGandham/MealBridge/blob/main/Screenshots/Screenshot%202025-03-08%20195408.png)

## API Endpoints (Manual URLs, No Router)

### Authentication
| Endpoint         | Method | Description          |
|-----------------|--------|----------------------|
| `/api/register/` | POST   | Register a new user |
| `/api/login/`   | POST   | Authenticate user    |

### Donee Endpoints
| Endpoint              | Method | Description |
|----------------------|--------|-------------|
| `/api/donees/`       | GET    | List all NGOs |
| `/api/donees/<id>/`  | GET    | Retrieve NGO details |

### Restaurant Endpoints
| Endpoint               | Method | Description |
|-----------------------|--------|-------------|
| `/api/restaurants/`    | GET    | List all restaurants |
| `/api/restaurants/<id>/` | GET  | Retrieve restaurant details |

### Food Donation Endpoints
| Endpoint                    | Method | Description |
|----------------------------|--------|-------------|
| `/api/donations/`           | GET    | List all food donations |
| `/api/donations/`           | POST   | Create a new donation |
| `/api/donations/<id>/`      | PATCH  | Update donation status |

## Installation Guide

### Prerequisites
- Python 3.8+
- Django 4+
- Django REST Framework
- PostgreSQL (or SQLite for local development)

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/yourusername/MealBridge.git
cd MealBridge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Added new feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Create a Pull Request


## Contact
For any inquiries, reach out at **gpranitha2003@gmail.com** or open an issue on GitHub.

---

🚀 **MealBridge** - Bridging the gap between surplus food & those in need!

