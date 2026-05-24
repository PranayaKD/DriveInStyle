from django import forms
from .models import Product, TestDriveBooking, Enquiry


class ProductEmiForm(forms.ModelForm):
    product_name = forms.CharField(disabled=True)
    price = forms.CharField(disabled=True)
    loan_amount = forms.IntegerField()
    tenure = forms.IntegerField(label="Tenure (years)")

    class Meta:
        model = Product
        fields = ['product_name', 'price']


class TestDriveForm(forms.ModelForm):
    product_name = forms.CharField(disabled=True)
    user_name = forms.CharField(disabled=True)
    phone = forms.CharField(disabled=True)
    email = forms.CharField(disabled=True)
    booking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time_slot = forms.ChoiceField(choices=[
        ('9AM - 11AM', '9AM - 11AM'),
        ('11AM - 1PM', '11AM - 1PM'),
        ('2PM - 4PM', '2PM - 4PM'),
        ('4PM - 6PM', '4PM - 6PM'),
    ])

    class Meta:
        model = TestDriveBooking
        fields = ['booking_date', 'time_slot']


class EnquiryForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}))
    
    class Meta:
        model = Enquiry
        fields = ['phone', 'message']
