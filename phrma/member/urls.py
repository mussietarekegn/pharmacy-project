from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('register/user/', views.customer_register, name='register_customer'),
    path('register/pharmacy/', views.pharmacy_register, name='register_pharmacy'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pharmacy/verify/list/', views.verify_pharmacy_list, name='verify_pharmacy_list'),
    path('pharmacy/approve/<int:profile_id>/', views.approve_pharmacy, name='approve_pharmacy'),
    path('dashboard/', views.pharmacy_dashboard, name='dashboard'),
    path('medicine/add/', views.add_medicine, name='add_medicine'),
    path('customer/welcome/', views.customer_welcome, name='customer_welcome'),  # new
    path('pharmacy/update/', views.update_profile, name='update_profile'),

]

