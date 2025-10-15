from django import forms
from .models import Products, Book_Test_Drive, Enquiry

# EMI Form
class ProductEmiForm(forms.ModelForm):
    product_name = forms.CharField(disabled=True)
    price = forms.CharField(disabled=True)
    loan_amount = forms.IntegerField()
    tensure = forms.IntegerField()

    class Meta:
        model = Products
        fields = ['product_name', 'price']

# Test Drive Form
class Test_Drive_Form(forms.ModelForm):
    product_name = forms.CharField(disabled=True)
    user_name = forms.CharField(disabled=True)
    phone = forms.CharField(disabled=True)
    email = forms.CharField(disabled=True)
    t_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time_slot = forms.ChoiceField(choices=[
        ('9AM - 11AM', '9AM - 11AM'),
        ('11AM - 1PM', '11AM - 1PM'),
        ('2PM - 4PM', '2PM - 4PM'),
        ('4PM - 6PM', '4PM - 6PM'),
    ])

    class Meta:
        model = Book_Test_Drive
        fields = ['t_date', 'time_slot']

# Enquiry Form
class EnquiryForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Your message...'}))
    
    class Meta:
        model = Enquiry
        fields = ['phone', 'message']
