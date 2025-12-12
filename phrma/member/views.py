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
from django.contrib import messages


def home(request):
    return render(request, "member/home.html")

def admin_required(user):
    return user.is_superuser

def customer_register(request):
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'customer'  
            user.save()
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    
    return render(request, 'member/customer_register.html', {'form': form})

def pharmacy_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        pharmacy_form = PharmacyOwnerForm(request.POST, request.FILES)

        if user_form.is_valid() and pharmacy_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'pharmacy_owner'
            user.save()

            profile = pharmacy_form.save(commit=False)
            profile.user = user
            profile.is_verified = False  

            messages.info(request, "Your pharmacy account is registered. Please wait for admin approval before logging in.")
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        pharmacy_form = PharmacyOwnerForm()

    return render(request, 'member/pharmacy_register.html', {
        'user_form': user_form,
        'pharmacy_form': pharmacy_form
    })


def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'pharmacy_owner':
            profile = getattr(request.user, 'pharmacyownerprofile', None)
            if profile and not profile.is_verified:
                return render(request, 'member/not_verified.html')
            return redirect('dashboard')
        elif request.user.role == 'customer':
            return redirect('customer_welcome')
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        role = request.POST.get('role')

        if form.is_valid():
            user = form.get_user()

            if user.role != role:
                form.add_error(None, "Selected role does not match your account role.")
            else:

                if role == 'pharmacy_owner':
                    profile = getattr(user, 'pharmacyownerprofile', None)
                    if profile and not profile.is_verified:
                        messages.warning(request, "Your pharmacy account is not verified yet. Please wait for admin approval.")
                        return render(request, 'member/not_verified.html')

                login(request, user)

                if role == 'pharmacy_owner':
                    return redirect('dashboard')
                elif role == 'customer':
                    return redirect('customer_welcome')
                else:
                    return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'member/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


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

            messages.success(request, "Medicine added successfully!")
            return redirect('dashboard')
    else:
        form = MedicineForm()

    return render(request, 'member/add_medicine.html', {'form': form})

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
@login_required
def customer_welcome(request):
    if request.user.role != 'customer':
        return redirect('login')

    query = request.GET.get('q', '')

    if query:
        medicines = Medicine.objects.filter(name__icontains=query)
    else:
        medicines = Medicine.objects.all()

    context = {
        'medicines': medicines,
        'query': query,
    }
    return render(request, 'member/customer_welcome.html', context)


@login_required
def medicine_detail(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request, 'member/medicine_detail.html', {'medicine': medicine})

@login_required
def edit_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if medicine.owner != request.user.pharmacyownerprofile:
        return redirect('dashboard')

    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, "Medicine updated successfully!")
            return redirect('dashboard')
    else:
        form = MedicineForm(instance=medicine)

    return render(request, 'member/edit_medicine.html', {'form': form, 'medicine': medicine})

@login_required
def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)

    if medicine.owner != request.user.pharmacyownerprofile:
        return redirect('dashboard')

    if request.method == 'POST':
        medicine.delete()
        messages.success(request, "Medicine deleted successfully!")
        return redirect('dashboard')

    return render(request, 'member/delete_medicine_confirm.html', {'medicine': medicine})
