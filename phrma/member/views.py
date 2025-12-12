from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import (
    CustomerRegisterForm,
    MedicineForm,
    PharmacyProfileForm,
    PharmacyOwnerForm,
    UserRegistrationForm
)
from .models import CustomUser, PharmacyOwnerProfile,Medicine
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm

# -----------------------------
# Helper Functions
# -----------------------------
def home(request):
    return render(request, "member/home.html")

def admin_required(user):
    return user.is_superuser

# -----------------------------
# Customer Registration
# -----------------------------
def customer_register(request):
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'  # explicitly set role
            user.save()
            # Redirect to login page after successful registration
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    
    return render(request, 'member/customer_register.html', {'form': form})

# -----------------------------
# Pharmacy Registration
# -----------------------------
def pharmacy_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        pharmacy_form = PharmacyOwnerForm(request.POST, request.FILES)

        if user_form.is_valid() and pharmacy_form.is_valid():
            # Save user
            user = user_form.save(commit=False)
            user.role = 'pharmacy_owner'
            user.save()

            # Save pharmacy profile
            profile = pharmacy_form.save(commit=False)
            profile.user = user
            profile.is_verified = False
            profile.save()

            # Redirect to login page
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        pharmacy_form = PharmacyOwnerForm()

    return render(request, 'member/pharmacy_register.html', {
        'user_form': user_form,
        'pharmacy_form': pharmacy_form
    })


# -----------------------------
# Login / Logout
# -----------------------------
def login_view(request):
    if request.user.is_authenticated:
        # Redirect based on role
        if request.user.role == 'pharmacy_owner':
            if hasattr(request.user, 'pharmacyownerprofile') and not request.user.pharmacyownerprofile.is_verified:
                return render(request, 'member/not_verified.html')
            return redirect('dashboard')
        elif request.user.role == 'customer':
            return redirect('customer_welcome')  # new view for customer
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        role = request.POST.get('role')

        if form.is_valid():
            user = form.get_user()

            if user.role != role:
                form.add_error(None, "Selected role does not match your account role.")
            else:
                login(request, user)

                if role == 'pharmacy_owner':
                    if not user.pharmacyownerprofile.is_verified:
                        logout(request)
                        return render(request, 'member/not_verified.html')
                    return redirect('dashboard')
                elif role == 'customer':
                    return redirect('customer_welcome')  # redirect customers
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'member/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

# -----------------------------
# Admin: Verify Pharmacies
# -----------------------------
@user_passes_test(admin_required)
def verify_pharmacy_list(request):
    unverified = PharmacyOwnerProfile.objects.filter(is_verified=False)
    return render(request, 'member/verify_pharmacy_list.html', {'pharmacies': unverified})

@user_passes_test(admin_required)
def approve_pharmacy(request, profile_id):
    profile = get_object_or_404(PharmacyOwnerProfile, id=profile_id)
    profile.is_verified = True
    profile.save()
    return redirect('verify_pharmacy_list')

# -----------------------------
# Pharmacy Dashboard
# -----------------------------
@login_required
def pharmacy_dashboard(request):
    if request.user.role != 'pharmacy_owner':
        return redirect('login')

    profile = request.user.pharmacyownerprofile
    if not profile.is_verified:
        return render(request, 'member/not_verified.html')

    medicines = profile.medicine_set.all()

    return render(request, 'member/pharmacy_dashboard.html', {
        'profile': profile,
        'medicines': medicines
    })

# -----------------------------
# Add Medicine
# -----------------------------
@login_required
def add_medicine(request):
    if request.user.role != 'pharmacy_owner' or not request.user.pharmacyownerprofile.is_verified:
        return redirect('login')

    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.owner = request.user.pharmacyownerprofile
            medicine.save()
            return redirect('dashboard')
    else:
        form = MedicineForm()

    return render(request, 'member/add_medicine.html', {'form': form})

# -----------------------------
# Update Pharmacy Profile
# -----------------------------
@login_required
def update_profile(request):
    profile = request.user.pharmacyownerprofile
    if request.method == 'POST':
        form = PharmacyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PharmacyProfileForm(instance=profile)

    return render(request, 'member/update_profile.html', {'form': form})

@login_required
def customer_welcome(request):
    if request.user.role != 'customer':
        return redirect('login')
    return render(request, 'member/customer_welcome.html', {'user': request.user})

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'member/medicine_list.html', {'medicines': medicines})
