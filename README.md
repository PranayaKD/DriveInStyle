# AutoSphere (djbtm2) — Automotive Dealership, Fleet Rental & Financial Engine

[![Django](https://img.shields.io/badge/Django-5.2.4-092e20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952b3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 1. Project Overview

**AutoSphere (djbtm2)** is an integrated automotive dealership showroom and short-term car rental engine built on Django 5.2. The platform bridges vehicle retail, test drive scheduling, financial estimation (amortized EMI and statutory on-road price breakdowns), with a distance-based car rental platform featuring dynamic rate calculation and automated email invoicing.

The application enforces a single source of truth for all pricing arithmetic via decoupled service layers, automatic idle-session timeout for security, Google reCAPTCHA bot prevention, and token-based email password recovery.

---

## 2. Tech Stack & Dependencies

| Category | Technology | Details |
|---|---|---|
| **Backend Framework** | Django 5.2.4 | MVT architecture, ORM, Session management |
| **Language** | Python 3 | Clean functional & service-oriented design |
| **Frontend UI** | HTML5, CSS3, Bootstrap 5 | Mobile-responsive showroom and rental catalog |
| **Form Formatting** | Django Crispy Forms & Crispy Bootstrap 5 | Semantic form layouts |
| **Security & Protection** | `django-recaptcha` & `django-auto-logout` | Bot defense on signup, automatic 120s idle session termination |
| **Database** | SQLite (Dev) / PostgreSQL (Production) | Dynamic resolution via `dj-database-url` |
| **Static & Media Delivery** | WhiteNoise 6.9.0 | Manifest-hashed caching for static assets, Django media pipeline |
| **Email Delivery** | Django SMTP Email Backend | Transactional rental bills and password reset tokens |
| **Deployment** | Gunicorn & WhiteNoise | Production deployment ready via `build.sh` |

---

## 3. Architecture & Domain Separation

The application is architected across three distinct business domain apps:

```
djbtm2/
├── manage.py                   # Django CLI management entry point
├── build.sh                    # Automated Render build script
├── requirements.txt            # Python dependencies
├── .env.example                # Environment configuration template
├── djbtm2/                     # Core project configuration
│   ├── settings.py             # Security settings, database URL config, session timeouts
│   ├── urls.py                 # Root URL router delegating across domain apps
│   ├── wsgi.py                 # WSGI entry point
│   └── asgi.py                 # ASGI entry point
├── btmapp/                     # User identity, KYC profile & authentication domain
│   ├── models.py               # UserRegistration (address, phone, avatar, signals)
│   ├── forms.py                # Registration, profile update, and login forms
│   ├── views.py                # Auth workflows (signup, login, profile, password reset)
│   ├── utils.py                # Transactional email dispatcher (rental billing)
│   └── urls.py                 # Account & authentication routing
├── carsapp/                    # Dealership showroom & financial calculators
│   ├── models.py               # Company, Product, ProductInterior/Exterior, TestDrive, Enquiry
│   ├── forms.py                # ProductEmiForm, TestDriveForm, EnquiryForm
│   ├── views.py                # Showroom catalog, EMI calculator, On-Road price, Test drives
│   └── urls.py                 # Dealership routing
├── rentalcars/                 # On-demand fleet rental booking domain
│   ├── models.py               # RentalCar (mileage, fuel, seating, amenities, ratings)
│   ├── services.py             # Pricing service (Single Source of Truth for rent calculation)
│   ├── views.py                # Fleet filtering, rent estimation, post-trip checkout
│   └── urls.py                 # Rental routing
├── templates/                  # Server-side HTML templates (showroom, rental, auth)
└── static/                     # CSS stylesheets, JavaScript files, and media assets
```

---

## 4. Key Engineering & Business Features

### 🧮 Amortized Loan EMI Calculator with Tiered Interest Rates
- Implements standard reducing-balance EMI loan formulas:
  $$EMI = \frac{P \times r \times (1 + r)^n}{(1 + r)^n - 1}$$
- Dynamic tenure-based interest rate tiers:
  - $\le 2$ Years: **8.5%**
  - $\le 4$ Years: **9.5%**
  - $\le 6$ Years: **10.5%**
  - $\le 8$ Years: **12.0%**
  - $> 8$ Years: **13.5%** (Default)

### 🧾 Comprehensive On-Road Pricing Breakdown
Calculates realistic vehicle acquisition costs including all statutory levies:
- **Ex-Showroom Price** (Base)
- **Road Tax**: 8.0%
- **RTO Charges**: 5.0%
- **GST**: 18.0%
- **Insurance**: 3.5%
- **Miscellaneous / Logistics**: 2.0%

### 🚘 Deterministic Fleet Rental Engine (`rentalcars/services.py`)
- **Single Source of Truth**: All rental math lives in isolated domain services, never duplicated inside views.
- **Tiered Fuel & Seating Matrix**:
  - Petrol: 5-Seater = ₹11/km | 7-Seater = ₹16/km
  - Diesel: 5-Seater = ₹9/km | 7-Seater = ₹14/km
- **Daily Minimum Guarantees**: Enforces a minimum base distance of 300 km/day.
- **Progressive Extra Distance Surcharges**:
  - $< 500$ extra km beyond allowed trip distance: +2% surcharge.
  - $\ge 500$ extra km beyond allowed trip distance: +4% surcharge.
- **Estimated User Fuel Expenditure**: Computes user fuel expenditure based on live fuel prices (Petrol ₹102/L, Diesel ₹96/L) and vehicle rated mileage.

### 🔒 Enterprise Security & Session Controls
- **Automated Idle Session Termination**: Sessions automatically terminate after 120 seconds of inactivity via `django-auto-logout`.
- **Bot Mitigation**: Google reCAPTCHA integrated directly onto registration endpoints.
- **Atomic User Profile Provisioning**: Uses Django `post_save` signals and `transaction.atomic()` during user registration to ensure `User` and `UserRegistration` profiles stay in sync without orphaned records.
- **Tokenized Password Reset**: Secure tokenized password recovery via SMTP email.

---

## 5. Database Schema & Data Models

### 1. `btmapp.models.UserRegistration`
- `user`: `OneToOneField(auth.User, on_delete=CASCADE, related_name='profile')`
- `phone`: `CharField(max_length=15)` (Validated: exactly 10 digits)
- `door_no`, `street`, `landmark`, `city`, `state`: Address fields
- `pincode`: `CharField(max_length=6)` (Validated: exactly 6 digits)
- `userpic`: `ImageField(upload_to="profiles/%Y/%m/", null=True, blank=True)`

### 2. `carsapp.models.Company` & `Product`
- **Company**: `name`, `ceo`, `est_year`, `origin`, `logo`
- **Product**: `product_name`, `color`, `seat_capacity`, `fuel_type`, `cc`, `mileage`, `price`, `prod_image`, `company` (ForeignKey)
- **ProductInteriorImage** & **ProductExteriorImage**: One-to-many galleries attached to each vehicle model.
- **TestDriveBooking**: Tracks user test drive reservations with assigned date and time slot.
- **Enquiry**: Captures user purchase inquiries and contact messages.

### 3. `rentalcars.models.RentalCar`
- `car_name`, `company`, `color`: Vehicle branding and model
- `fuel_type`: Choice (`Petrol`, `Diesel`, `CNG`, `EV`)
- `seat_capacity`: Choice (`5 Seater`, `7 Seater`)
- `transmission_type`: Choice (`Manual`, `Automatic`)
- `mileage`: Rated km per litre
- `total_km_driven`: Baseline odometer reading
- `amenities`, `bootspace`, `rating`, `car_img`: Features and media

---

## 6. Complete URL Routing & Endpoints

| Domain | HTTP Method | URL Path | Description | Access |
|---|---|---|---|---|
| **Auth** | `GET` | `/` | Showroom and rental landing portal | Public |
| **Auth** | `GET`, `POST` | `/register/` | User registration with reCAPTCHA verification | Public |
| **Auth** | `GET`, `POST` | `/login/` | User authentication with idle session tracking | Public |
| **Auth** | `GET`, `POST` | `/logout/` | User logout and session termination | Authenticated |
| **Auth** | `GET` | `/profile/` | User account details and address view | Authenticated |
| **Auth** | `GET`, `POST` | `/profile/update/` | Edit user profile and address information | Authenticated |
| **Auth** | `GET`, `POST` | `/password-reset/` | Request tokenized password reset email | Public |
| **Dealership** | `GET` | `/comp/` | List all automobile manufacturers | Public |
| **Dealership** | `GET` | `/comp/<id>/` | View models produced by a specific manufacturer | Public |
| **Dealership** | `GET` | `/comp/product/<id>/` | Detailed car specs with interior/exterior gallery | Public |
| **Dealership** | `GET`, `POST` | `/comp/calcemi/<id>/` | Interactive EMI loan computation | Authenticated |
| **Dealership** | `GET` | `/comp/finalprice/<id>/` | Full on-road tax, RTO, and insurance breakdown | Public |
| **Dealership** | `GET`, `POST` | `/comp/booktestdrive/<id>/` | Schedule test drive date and time slot | Authenticated |
| **Dealership** | `GET`, `POST` | `/comp/enquiry/` | Submit vehicle purchasing enquiry | Authenticated |
| **Rental** | `GET` | `/rental/` | Rental fleet landing and seating selection | Public |
| **Rental** | `GET` | `/rental/<seat_capacity>/` | Filter rental fleet by 5 or 7 seater vehicles | Public |
| **Rental** | `GET` | `/rental/detail/<car_id>/` | Full rental car specification and features | Public |
| **Rental** | `GET`, `POST` | `/rental/calculate/<car_id>/` | Pre-trip estimated rental quote based on days & km | Public |
| **Rental** | `GET`, `POST` | `/rental/final_price/<car_id>/` | Post-trip final checkout & automatic billing email | Public |
| **Admin** | `GET`, `POST` | `/admin/` | Django administrative operations | Staff / Admin |

---

## 7. Environment Variables Reference

Create a `.env` file in the root directory:

```env
# Security
SECRET_KEY=your-production-secret-key
DEBUG=True

# Hostnames (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

# Database (Optional: falls back to local SQLite if omitted)
# DATABASE_URL=postgres://user:password@localhost:5432/djbtm2_db

# Google reCAPTCHA v2 / v3
RECAPTCHA_PUBLIC_KEY=your_recaptcha_public_key
RECAPTCHA_PRIVATE_KEY=your_recaptcha_private_key

# Transactional Email (Gmail SMTP / SendGrid)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

---

## 8. Local Setup & Installation

### Step-by-Step Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PranayaKD/Rentora.git
   cd djbtm2
   ```

2. **Set up a virtual environment**:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Update .env with your local settings
   ```

5. **Execute database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create an administrative superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 9. Running Test Suites

Execute comprehensive test coverage across user authentication, car dealership calculators, and the rental pricing service:

```bash
python manage.py test btmapp carsapp rentalcars -v 2
```

---

## 10. Production Deployment

The project contains a pre-configured `build.sh` script for Render or similar PaaS providers:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Start the application with Gunicorn:
```bash
gunicorn djbtm2.wsgi:application
```
