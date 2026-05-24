# btmapp/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserRegistration
from .forms import UserForm, UserProfileForm, UserUpdateForm, UserProfileUpdateForm


class UserRegistrationModelTest(TestCase):
    """Tests for the UserRegistration model."""

    def test_profile_created_on_user_creation(self):
        """Signal should auto-create a profile when a User is created."""
        user = User.objects.create_user(username='testuser', password='TestPass123!')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, UserRegistration)

    def test_profile_str_representation(self):
        """Profile __str__ should return '<username>'s Profile'."""
        user = User.objects.create_user(username='john', password='TestPass123!')
        self.assertEqual(str(user.profile), "john's Profile")

    def test_full_address_with_all_fields(self):
        """full_address should format all parts correctly."""
        user = User.objects.create_user(username='addr_user', password='TestPass123!')
        profile = user.profile
        profile.door_no = '42'
        profile.street = 'MG Road'
        profile.landmark = 'Near Mall'
        profile.city = 'Bangalore'
        profile.state = 'Karnataka'
        profile.pincode = '560001'
        profile.save()
        self.assertIn('42', profile.full_address)
        self.assertIn('560001', profile.full_address)

    def test_full_address_empty(self):
        """full_address should return default when no fields are set."""
        user = User.objects.create_user(username='empty_user', password='TestPass123!')
        self.assertEqual(user.profile.full_address, "No address provided")

    def test_display_phone_formatted(self):
        """display_phone should format a 10-digit phone number."""
        user = User.objects.create_user(username='phone_user', password='TestPass123!')
        user.profile.phone = '9876543210'
        user.profile.save()
        self.assertIn('+91', user.profile.display_phone)

    def test_display_phone_empty(self):
        """display_phone should handle empty phone gracefully."""
        user = User.objects.create_user(username='no_phone', password='TestPass123!')
        self.assertEqual(user.profile.display_phone, "Not provided")


class UserFormTest(TestCase):
    """Tests for the UserForm (registration form)."""

    def test_valid_registration(self):
        """Form should be valid with correct data."""
        form = UserForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        """Form should reject mismatched passwords."""
        form = UserForm(data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'StrongPass123!',
            'confirm_password': 'DifferentPass456!',
        })
        self.assertFalse(form.is_valid())

    def test_duplicate_username(self):
        """Form should reject duplicate usernames."""
        User.objects.create_user(username='existing', password='TestPass123!')
        form = UserForm(data={
            'username': 'existing',
            'email': 'unique@example.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_duplicate_email(self):
        """Form should reject duplicate emails."""
        User.objects.create_user(username='user1', email='dup@example.com', password='TestPass123!')
        form = UserForm(data={
            'username': 'user2',
            'email': 'dup@example.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_weak_password(self):
        """Form should reject weak passwords."""
        form = UserForm(data={
            'username': 'weakpw',
            'email': 'weak@example.com',
            'password': '123',
            'confirm_password': '123',
        })
        self.assertFalse(form.is_valid())


class AuthViewTest(TestCase):
    """Tests for authentication views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )

    def test_home_page_loads(self):
        """Home page should load for anonymous users."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_registration_page_loads(self):
        """Registration page should load for anonymous users."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        """Login page should load for anonymous users."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Valid credentials should log the user in."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_login_failure(self):
        """Invalid credentials should show error."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, 200)  # Stays on login page

    def test_profile_requires_login(self):
        """Profile page should redirect anonymous users to login."""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_profile_loads_for_authenticated(self):
        """Profile page should load for authenticated users."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Logout should redirect to login page."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_redirected_from_login(self):
        """Already authenticated users should be redirected from login page."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_password_reset_page_loads(self):
        """Password reset page should be accessible."""
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
