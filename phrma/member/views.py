from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from.forms import CustomerRegisterForm,PharmacyOwnerRegisterForm
# Create your views here.

def customer_register(request):
    form=CustomerRegisterForm()
    if request.method=="POST":
        form=CustomerRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect ('/')
    return render(request,'member/customer_register.html',{'form':form})

def pharmacy_register(request):
    form=PharmacyOwnerRegisterForm()
    if request.method=="POST":
        form=PharmacyOwnerRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.role='pharmacy_owner'
            user.save()
            login(request,user)
            return redirect('/')
    return render(request,'member/pharmacy_register.html',{'form':form})

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
    return render(request,'member/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

