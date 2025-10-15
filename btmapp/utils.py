from django.core.mail import send_mail  
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email_view(email, car_name, exp_km, final_price):
    subject = 'Booking Successful - Your Car Rental Bill'
    message = 'Thank you for booking a car in Drive in Style. Chase your dreams with us.'
    from_email = 'dashpranaya786@gmail.com'
    recipient_list = [email]

    html_message = render_to_string('bill_email_template.html', {
        'car_name': car_name,
        'exp_km': exp_km,
        'final_price': final_price,
        'email': email,
    })
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False