# btmapp/utils.py
"""
Utility functions for btmapp
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_email_view(email, car_name, exp_km, final_price):
    """
    Send rental bill email to customer
    
    Args:
        email (str): Customer email address
        car_name (str): Name of the rented car
        exp_km (int): Final kilometer reading
        final_price (float): Final rental price
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if not email:
        logger.warning("Email sending attempted with no recipient email")
        return False
    
    try:
        subject = 'Booking Successful - Your Car Rental Bill'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        
        # Render HTML template
        html_message = render_to_string('bill_email_template.html', {
            'car_name': car_name,
            'exp_km': exp_km,
            'final_price': final_price,
            'email': email,
        })
        
        # Create plain text version
        plain_message = strip_tags(html_message)
        
        # Create email with both HTML and plain text versions
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=from_email,
            to=recipient_list
        )
        
        # Attach HTML version
        email_message.attach_alternative(html_message, "text/html")
        
        # Send email
        email_message.send(fail_silently=False)
        
        logger.info(f"Rental bill email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}")
        return False


def send_welcome_email(user_email, username):
    """
    Send welcome email to newly registered users
    
    Args:
        user_email (str): User's email address
        username (str): User's username
        
    Returns:
        bool: True if email sent successfully
    """
    try:
        subject = 'Welcome to CarRental - Drive Your Dreams!'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # You can create a welcome email template
        message = f"""
        Dear {username},
        
        Welcome to CarRental! We're excited to have you on board.
        
        You can now:
        - Browse our extensive fleet of vehicles
        - Book cars for rent
        - Purchase your dream car
        - Track your bookings
        
        If you have any questions, feel free to contact our support team.
        
        Happy driving!
        
        Best regards,
        The CarRental Team
        """
        
        from django.core.mail import send_mail
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user_email],
            fail_silently=True
        )
        
        logger.info(f"Welcome email sent to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
        return False


def send_password_reset_notification(user_email, username):
    """
    Send notification when password is reset
    
    Args:
        user_email (str): User's email address
        username (str): User's username
        
    Returns:
        bool: True if email sent successfully
    """
    try:
        subject = 'Password Reset Successful - CarRental'
        from_email = settings.DEFAULT_FROM_EMAIL
        
        message = f"""
        Dear {username},
        
        Your password has been reset successfully.
        
        If you did not make this change, please contact our support team immediately.
        
        Best regards,
        The CarRental Team
        """
        
        from django.core.mail import send_mail
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user_email],
            fail_silently=True
        )
        
        logger.info(f"Password reset notification sent to {user_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset notification to {user_email}: {str(e)}")
        return False