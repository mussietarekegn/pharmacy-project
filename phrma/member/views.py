from django.shortcuts import redirect, get_object_or_404,render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView
)
from .forms import (
    CustomerRegisterForm,
    MedicineForm,
    PharmacyProfileForm,
    PharmacyOwnerForm,
    UserRegistrationForm,
    CustomerProfileForm
)
from .models import CustomUser, PharmacyOwnerProfile, Medicine


class HomeView(TemplateView):
    template_name = "member/home.html"


class CustomerRegisterView(CreateView):
    form_class = CustomerRegisterForm
    template_name = "member/customer_register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = "customer"
        user.save()
        return super().form_valid(form)


class PharmacyRegisterView(CreateView):
    template_name = "member/pharmacy_register.html"
    form_class = UserRegistrationForm  # Handles the user account part
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide both forms in context for GET request
        if "user_form" not in context:
            context["user_form"] = UserRegistrationForm()
        if "pharmacy_form" not in context:
            context["pharmacy_form"] = PharmacyOwnerForm()
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserRegistrationForm(request.POST)
        pharmacy_form = PharmacyOwnerForm(request.POST, request.FILES)

        if user_form.is_valid() and pharmacy_form.is_valid():
            # Save the user account
            user = user_form.save(commit=False)
            user.role = "pharmacy_owner"
            user.save()

            # Save the pharmacy profile
            profile = pharmacy_form.save(commit=False)
            profile.user = user
            profile.is_verified = False
            profile.save()

            messages.success(
                request,
                "Your pharmacy account is registered. Please wait for admin approval before logging in."
            )
            return redirect("login")

        # If invalid, render both forms with errors
        context = self.get_context_data()
        context["user_form"] = user_form
        context["pharmacy_form"] = pharmacy_form
        return self.render_to_response(context)
def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == "pharmacy_owner":
            profile = getattr(request.user, "pharmacyownerprofile", None)
            if profile and not profile.is_verified:
                return redirect("not_verified")
            return redirect("dashboard")
        elif request.user.role == "customer":
            return redirect("customer_welcome")
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        role = request.POST.get("role")
        if form.is_valid():
            user = form.get_user()
            if user.role != role:
                form.add_error(None, "Selected role does not match your account role.")
            else:
                if role == "pharmacy_owner":
                    profile = getattr(user, "pharmacyownerprofile", None)
                    if profile and not profile.is_verified:
                        messages.warning(
                            request,
                            "Your pharmacy account is not verified yet. Please wait for admin approval."
                        )
                        return redirect("not_verified")
                login(request, user)
                if role == "pharmacy_owner":
                    return redirect("dashboard")
                else:
                    return redirect("customer_welcome")
    else:
        form = AuthenticationForm()
    return render(request, "member/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")

def admin_required(user):
    return user.is_superuser


@user_passes_test(admin_required)
def verify_pharmacy_list(request):
    unverified = PharmacyOwnerProfile.objects.filter(is_verified=False)
    return render(request, "member/verify_pharmacy_list.html", {"pharmacies": unverified})


@user_passes_test(admin_required)
def approve_pharmacy(request, profile_id):
    profile = get_object_or_404(PharmacyOwnerProfile, id=profile_id)
    profile.is_verified = True
    profile.save()
    return redirect("verify_pharmacy_list")


@method_decorator(login_required, name="dispatch")
class PharmacyDashboardView(TemplateView):
    template_name = "member/pharmacy_dashboard.html"

    def get(self, request, *args, **kwargs):
        if request.user.role != "pharmacy_owner":
            return redirect("login")
        profile = request.user.pharmacyownerprofile
        if not profile.is_verified:
            return redirect("not_verified")
        context = {"profile": profile, "medicines": profile.medicine_set.all()}
        return self.render_to_response(context)


@method_decorator(login_required, name="dispatch")
class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "member/add_medicine.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.owner = self.request.user.pharmacyownerprofile
        messages.success(self.request, "Medicine added successfully!")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class MedicineUpdateView(UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = "member/edit_medicine.html"
    pk_url_kwarg = "medicine_id"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user.pharmacyownerprofile:
            return redirect("dashboard")
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Medicine updated successfully!")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = "member/delete_medicine_confirm.html"
    pk_url_kwarg = "medicine_id"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user.pharmacyownerprofile:
            return redirect("dashboard")
        return obj


class MedicineDetailView(DetailView):
    model = Medicine
    template_name = "member/medicine_detail.html"
    pk_url_kwarg = "medicine_id"


class MedicineListView(ListView):
    model = Medicine
    template_name = "member/medicine_list.html"
    context_object_name = "medicines"


@method_decorator(login_required, name="dispatch")
class PharmacyProfileUpdateView(UpdateView):
    model = PharmacyOwnerProfile
    form_class = PharmacyProfileForm
    template_name = "member/update_profile.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user.pharmacyownerprofile


@method_decorator(login_required, name="dispatch")
class CustomerProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomerProfileForm
    template_name = "member/update_customer_profile.html"
    success_url = reverse_lazy("customer_welcome")

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required, name="dispatch")
class CustomerWelcomeView(ListView):
    model = Medicine
    template_name = "member/customer_welcome.html"
    context_object_name = "medicines"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        if query:
            return Medicine.objects.filter(name__icontains=query)
        return Medicine.objects.all()

def not_verified_view(request):
    return render(request, "member/not_verified.html")