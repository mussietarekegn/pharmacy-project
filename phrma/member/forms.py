from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,PharmacyOwnerProfile,Medicine

class CustomerRegisterForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','email','password1','password2']

# class PharmacyRegisterForm(forms.ModelForm):

#     username=forms.CharField(max_length=150)
#     email=forms.EmailField()
#     password=forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model=PharmacyOwnerProfile
#         fields=['pharmacy_name','location','phone','verification_document']

class MedicineForm(forms.ModelForm):
    class Meta:
        model=Medicine
        fields=['name','category','description','image','price','stock']
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
        exclude = ['user', 'is_verified']   # EXCLUDE USER
