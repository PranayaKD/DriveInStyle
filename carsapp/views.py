from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company, Product, TestDriveBooking, Enquiry
from .forms import ProductEmiForm, TestDriveForm, EnquiryForm
import math


def company_list(request):
    companies = Company.objects.all()
    return render(request, "cars/CompanyList.html", {"companies": companies})


def company_details(request, id=0):
    company = get_object_or_404(Company, id=id)
    return render(request, "cars/companydetails.html", {"company": company})


@login_required(login_url='login')
def calculate_emi(request, id=0):
    product = get_object_or_404(Product, id=id)
    emi = None

    if request.method == 'POST':
        form = ProductEmiForm(request.POST, instance=product)
        if form.is_valid():
            loan_amount = form.cleaned_data.get('loan_amount')
            tenure = form.cleaned_data.get('tenure')

            # Interest rate tiers based on loan tenure (years)
            INTEREST_TIERS = [
                (2, 8.5),
                (4, 9.5),
                (6, 10.5),
                (8, 12.0),
            ]
            DEFAULT_INTEREST_RATE = 13.5

            interest_rate = DEFAULT_INTEREST_RATE
            for max_years, rate in INTEREST_TIERS:
                if tenure <= max_years:
                    interest_rate = rate
                    break

            try:
                monthly_rate = interest_rate / 12 / 100
                total_months = tenure * 12
                emi = (loan_amount * monthly_rate * math.pow(1 + monthly_rate, total_months)) / \
                      (math.pow(1 + monthly_rate, total_months) - 1)
                emi = round(emi, 2)
            except (ZeroDivisionError, ValueError, OverflowError):
                emi = None
    else:
        form = ProductEmiForm(instance=product)

    return render(request, 'cars/emi.html', {'form': form, 'emi': emi})


def product_detail(request, id=0):
    product = get_object_or_404(Product, id=id)
    interior_images = product.interior_images.all()
    exterior_images = product.exterior_images.all()
    return render(request, "cars/product_detail.html", {
        "product": product,
        "interior_images": interior_images,
        "exterior_images": exterior_images
    })


def final_price(request, id=0):
    product = get_object_or_404(Product, id=id)
    price = product.price

    TAX_RATES = {
        'road_tax': 0.08,
        'rto_charges': 0.05,
        'gst': 0.18,
        'insurance': 0.035,
        'miscellaneous': 0.02,
    }

    breakdown = {key: round(price * rate, 2) for key, rate in TAX_RATES.items()}
    total = round(price + sum(breakdown.values()), 2)

    context = {
        "product": product,
        **breakdown,
        "final_price": total,
    }
    return render(request, "cars/product_final_price.html", context)


@login_required(login_url="login")
def book_test_drive(request, id=0):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = TestDriveForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.product = product
            booking.user = request.user.profile
            booking.save()
            return render(request, "cars/book_test_drive.html", {"confirmed": True, "product": product})
    else:
        form = TestDriveForm(initial={
            "product_name": product.product_name,
            "user_name": request.user.username,
            "email": request.user.email,
            "phone": request.user.profile.phone
        })
    return render(request, "cars/book_test_drive.html", {"form": form, "product": product})


@login_required(login_url="login")
def make_enquiry(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.user = request.user.profile
            enquiry.save()
            return render(request, "cars/enquiry_success.html", {"enquiry": enquiry})
    else:
        form = EnquiryForm(initial={'phone': request.user.profile.phone})
    return render(request, "cars/make_enquiry.html", {"form": form})
