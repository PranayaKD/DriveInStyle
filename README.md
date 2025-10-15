🏎️ DriveInStyle

DriveInStyle is a Django-based car rental and dealership management platform designed to provide a seamless experience for customers to explore, rent, and inquire about cars.
It features user authentication, car listings, booking management, and EMI price calculations — all within a responsive web interface.

🚀 Features

🔐 User Authentication – Registration, Login, Profile Management

🚘 Car Listings – Browse available cars with detailed specs and images

📅 Car Booking System – Book or rent vehicles with real-time availability

💰 EMI & Price Calculation – Automatic EMI and final price computation

📩 Email Confirmation – Booking confirmation emails sent to users

📊 Admin Dashboard – Manage users, cars, and bookings efficiently

📱 Responsive UI – Built with Bootstrap 5 for a clean modern design

🛠️ Tech Stack
Category	Technology
Backend	Django, Python
Frontend	HTML5, CSS3, Bootstrap 5, JavaScript
Database	SQLite / PostgreSQL
Version Control	Git & GitHub
Tools	VS Code, Virtualenv
⚙️ Setup Instructions

Clone the repository

git clone https://github.com/PranayaKD/DriveInStyle.git
cd DriveInStyle


Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate     # for Windows
# or
source venv/bin/activate  # for Mac/Linux


Install dependencies

pip install -r requirements.txt


Apply migrations

python manage.py makemigrations
python manage.py migrate


Run the development server

python manage.py runserver


Open your browser and visit:

http://127.0.0.1:8000/

📂 Project Structure
DriveInStyle/
├── manage.py
├── requirements.txt
├── djbtm2/                # Project settings and configuration
├── btmapp/                # User management and registration
├── carsapp/               # Car listings and enquiries
├── rentalcars/            # Car rental management
├── templates/             # HTML templates
└── static/ (optional)     # Static assets like CSS/JS/images

🧠 Future Improvements

🚗 Add payment gateway integration

📍 Include Google Maps API for pickup/drop locations

🌐 Deploy on Render or AWS

📈 Add analytics for car rentals and trends
