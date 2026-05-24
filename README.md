# 🚗 Rentora

Rentora is a Django-based car rental and dealership management platform designed to provide a seamless experience for customers to explore, rent, and inquire about cars.
It features user authentication, car listings, booking management, and EMI price calculations — all within a responsive web interface.

## 🚀 Features

- 🔐 **User Authentication** – Registration, Login, Profile Management, Secure Password Reset
- 🚘 **Car Listings** – Browse available cars with detailed specs and images
- 📅 **Car Booking System** – Book test drives and rent vehicles
- 💰 **EMI & Price Calculation** – Automatic EMI and final price computation
- 📩 **Email Confirmation** – Booking confirmation emails sent to users
- 📊 **Admin Dashboard** – Manage users, cars, and bookings efficiently
- 📱 **Responsive UI** – Built with Bootstrap 5 for a clean modern design

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Django 5.2, Python 3 |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Deployment | Render, WhiteNoise, Gunicorn |
| Version Control | Git & GitHub |

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/PranayaKD/Rentora.git
   cd Rentora
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate     # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser and visit:** http://127.0.0.1:8000/

## 🧪 Running Tests

```bash
python manage.py test btmapp carsapp rentalcars -v 2
```

## 📂 Project Structure

```
Rentora/
├── manage.py
├── requirements.txt
├── .env.example
├── djbtm2/                # Project settings and configuration
├── btmapp/                # User management and registration
│   ├── models.py          # UserRegistration model
│   ├── views.py           # Auth views (login, register, profile)
│   ├── forms.py           # User & profile forms
│   ├── utils.py           # Email utilities
│   └── tests.py           # Auth & model tests
├── carsapp/               # Car listings and enquiries
│   ├── models.py          # Company, Product, TestDriveBooking, Enquiry
│   ├── views.py           # Car browsing, EMI calc, test drive booking
│   ├── forms.py           # EMI, test drive, enquiry forms
│   └── tests.py           # Car model & view tests
├── rentalcars/            # Car rental management
│   ├── models.py          # RentalCar model
│   ├── services.py        # Pricing logic (single source of truth)
│   ├── views.py           # Rental views
│   └── tests.py           # Pricing & rental tests
├── templates/             # HTML templates
└── static/                # Static assets (CSS, images)
```

## 🔒 Security

- Password reset uses Django's built-in token-based email verification
- reCAPTCHA on registration to prevent spam
- Auto-logout after idle timeout
- CSRF protection on all forms
- Security headers enabled in production (HSTS, XSS filter, etc.)

## 🧠 Future Improvements

- 🚗 Add payment gateway integration
- 📍 Include Google Maps API for pickup/drop locations
- 🌐 Deploy on Render or AWS
- 📈 Add analytics for car rentals and trends
