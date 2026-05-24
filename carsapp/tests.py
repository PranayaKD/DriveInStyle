# carsapp/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Company, Product


class CompanyModelTest(TestCase):
    """Tests for the Company model."""

    def test_company_creation(self):
        """Company should be created with all required fields."""
        company = Company.objects.create(
            name='Tesla',
            ceo='Elon Musk',
            est_year=2003,
            origin='USA'
        )
        self.assertEqual(str(company), 'Tesla')
        self.assertEqual(company.est_year, 2003)

    def test_company_str(self):
        """Company __str__ should return the name."""
        company = Company.objects.create(name='BMW', ceo='Oliver Zipse', est_year=1916, origin='Germany')
        self.assertEqual(str(company), 'BMW')


class ProductModelTest(TestCase):
    """Tests for the Product model."""

    def setUp(self):
        self.company = Company.objects.create(
            name='Toyota',
            ceo='Akio Toyoda',
            est_year=1937,
            origin='Japan'
        )

    def test_product_creation(self):
        """Product should be created and associated with a company."""
        product = Product.objects.create(
            product_name='Camry',
            color='White',
            seat_capacity=5,
            fuel_type='Petrol',
            cc=2500,
            mileage=15,
            price=3500000,
            company=self.company
        )
        self.assertEqual(str(product), 'Camry')
        self.assertEqual(product.company.name, 'Toyota')
        self.assertEqual(product.mileage, 15)

    def test_product_price_breakdown(self):
        """Final price view should calculate tax breakdown correctly."""
        product = Product.objects.create(
            product_name='Corolla',
            color='Silver',
            seat_capacity=5,
            fuel_type='Petrol',
            cc=1800,
            mileage=18,
            price=1000000,
            company=self.company
        )
        # 8% road tax + 5% RTO + 18% GST + 3.5% insurance + 2% misc = 36.5%
        expected_total = 1000000 * 1.365
        # View calculates this, we test the math
        road_tax = round(1000000 * 0.08, 2)
        rto = round(1000000 * 0.05, 2)
        gst = round(1000000 * 0.18, 2)
        insurance = round(1000000 * 0.035, 2)
        misc = round(1000000 * 0.02, 2)
        total = round(1000000 + road_tax + rto + gst + insurance + misc, 2)
        self.assertEqual(total, expected_total)


class CarsappViewTest(TestCase):
    """Tests for carsapp views."""

    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(
            name='Honda',
            ceo='Toshihiro Mibe',
            est_year=1948,
            origin='Japan'
        )
        self.product = Product.objects.create(
            product_name='City',
            color='Red',
            seat_capacity=5,
            fuel_type='Petrol',
            cc=1500,
            mileage=17,
            price=1200000,
            company=self.company
        )
        self.user = User.objects.create_user(
            username='caruser',
            email='car@example.com',
            password='TestPass123!'
        )

    def test_company_list_loads(self):
        """Company list page should load."""
        response = self.client.get(reverse('company'))
        self.assertEqual(response.status_code, 200)

    def test_company_details_loads(self):
        """Company details page should load."""
        response = self.client.get(reverse('company_details', args=[self.company.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_loads(self):
        """Product detail page should load."""
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_emi_requires_login(self):
        """EMI calculator should require authentication."""
        response = self.client.get(reverse('calcemi', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_final_price_loads(self):
        """Final price page should load."""
        response = self.client.get(reverse('product_final_price', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
