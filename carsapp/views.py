from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company, Products, Book_Test_Drive, Enquiry
from .forms import ProductEmiForm, Test_Drive_Form, EnquiryForm
import math

@login_required(login_url="login")
def company_list(request):
    companies = Company.objects.all()
    return render(request, "cars/CompanyList.html", {"comp_name": companies})

@login_required(login_url="login")
def company_details(request, id=0):
    company = get_object_or_404(Company, id=id)
    return render(request, "cars/companydetails.html", {"company": company})

@login_required(login_url='login')
def calcemi(request, id=0):
    product = get_object_or_404(Products, id=id)
    emi = None
    if request.method == 'POST':
        form = ProductEmiForm(request.POST, instance=product)
        if form.is_valid():
            loan_amount = form.cleaned_data.get('loan_amount')
            tenure = form.cleaned_data.get('tensure')
            interest_rate = 10.0  # default
            if 1 <= tenure <= 2: interest_rate = 8.5
            elif 3 <= tenure <= 4: interest_rate = 9.5
            elif 5 <= tenure <= 6: interest_rate = 10.5
            elif 7 <= tenure <= 8: interest_rate = 12
            elif tenure >= 9: interest_rate = 13.5
            try:
                monthly_rate = interest_rate / 12 / 100
                total_months = tenure * 12
                emi = (loan_amount * monthly_rate * math.pow(1 + monthly_rate, total_months)) / \
                      (math.pow(1 + monthly_rate, total_months) - 1)
                emi = round(emi, 2)
            except:
                emi = None
    else:
        form = ProductEmiForm(instance=product)
    return render(request, 'cars/emi.html', {'form': form, 'emi': emi})

@login_required(login_url="login")
def product_detail(request, id=0):
    product = get_object_or_404(Products, id=id)
    interior_images = product.interior_images.all()
    exterior_images = product.exterior_images.all()
    return render(request, "cars/product_detail.html", {
        "product": product,
        "interior_images": interior_images,
        "exterior_images": exterior_images
    })

@login_required(login_url="login")
def final_price(request, id=0):
    product = get_object_or_404(Products, id=id)
    price = product.price
    road_tax = round(price * 0.08, 2)
    rto_charges = round(price * 0.05, 2)
    gst = round(price * 0.18, 2)
    insurance = round(price * 0.035, 2)
    misc = round(price * 0.02, 2)
    final_price = round(price + road_tax + rto_charges + gst + insurance + misc, 2)
    return render(request, "cars/product_final_price.html", {
        "product": product,
        "road_tax": road_tax,
        "rto_charges": rto_charges,
        "gst": gst,
        "insurance": insurance,
        "misc": misc,
        "final_price": final_price
    })

@login_required(login_url="login")
def Book_Test_Drive_views(request, id=0):
    product = get_object_or_404(Products, id=id)
    if request.method == "POST":
        form = Test_Drive_Form(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.product_name = product
            booking.user = request.user.userregisteration
            booking.save()
            return render(request, "cars/book_test_drive.html", {"confirmed": True, "product": product})
    else:
        form = Test_Drive_Form(initial={
            "product_name": product.product_name,
            "user_name": request.user.username,
            "email": request.user.email,
            "phone": request.user.userregisteration.phone
        })
    return render(request, "cars/book_test_drive.html", {"form": form, "product": product})

@login_required(login_url="login")
def make_enquiry(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.user = request.user.userregisteration
            enquiry.save()
            return render(request, "cars/enquiry_success.html", {"enquiry": enquiry})
    else:
        form = EnquiryForm(initial={'phone': request.user.userregisteration.phone})
    return render(request, "cars/make_enquiry.html", {"form": form})
