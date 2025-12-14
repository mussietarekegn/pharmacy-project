from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser,PharmacyOwnerProfile,Medicine

class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','email','password1','password2']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name','price','stock','image','expiry_date','location', 'description',  ]

        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
class PharmacyProfileForm(forms.ModelForm):
    class Meta:
        model = PharmacyOwnerProfile
        fields = ['pharmacy_name', 'location', 'phone', 'verification_document']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class PharmacyOwnerForm(forms.ModelForm):
    class Meta:
        model = PharmacyOwnerProfile
        exclude = ['user', 'is_verified']   

class CustomerProfileForm(UserChangeForm):
    # Only allow the user to update their username, email, etc.
    class Meta:
        model = CustomUser
        fields = ['username', 'email']