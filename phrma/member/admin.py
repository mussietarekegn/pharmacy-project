from django.contrib import admin
from .models import Medicine,CustomUser,PharmacyOwnerProfile
# Register your models here.

admin.site.register(Medicine)
admin.site.register(CustomUser)
admin.site.register(PharmacyOwnerProfile)
