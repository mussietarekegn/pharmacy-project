from django.urls import path
from . import views

urlpatterns=[
    path('register/user/',views.customer_register,name='register_customer'),
    path('register/pharmacy/',views.pharmacy_register,name='register_pharmacy'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
]