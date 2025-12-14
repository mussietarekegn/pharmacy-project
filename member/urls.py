from django.urls import path
from .views import *

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("register/user/", CustomerRegisterView.as_view(), name="register_customer"),
    path("register/pharmacy/", PharmacyRegisterView.as_view(), name="register_pharmacy"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("pharmacy/verify/list/", verify_pharmacy_list, name="verify_pharmacy_list"),
    path("pharmacy/approve/<int:profile_id>/", approve_pharmacy, name="approve_pharmacy"),

    path("dashboard/", PharmacyDashboardView.as_view(), name="dashboard"),
    path("medicine/add/", MedicineCreateView.as_view(), name="add_medicine"),
    path("medicine/<int:medicine_id>/edit/", MedicineUpdateView.as_view(), name="edit_medicine"),
    path("medicine/<int:medicine_id>/delete/", MedicineDeleteView.as_view(), name="delete_medicine"),
    path("medicine/<int:medicine_id>/", MedicineDetailView.as_view(), name="medicine_detail"),
    path("medicine/list/", MedicineListView.as_view(), name="medicine_list"),
    path("pharmacy/update/", PharmacyProfileUpdateView.as_view(), name="update_profile"),

    path("customer/welcome/", CustomerWelcomeView.as_view(), name="customer_welcome"),
    path("customer/profile/update/", CustomerProfileUpdateView.as_view(), name="update_customer_profile"),
    path('not_verified/', not_verified_view, name='not_verified'),
]
