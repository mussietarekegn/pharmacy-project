from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('pharmacy_owner', 'Pharmacy Owner'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    def __str__(self):
        return self.username


class PharmacyOwnerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pharmacy_name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    verification_document = models.FileField(upload_to='verification_docs/')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pharmacy_name} - {self.user.username}"


class Medicine(models.Model):
    owner = models.ForeignKey(PharmacyOwnerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='medicine_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    expiry_date = models.DateField(null=True, blank=True)  # NEW
    location = models.CharField(max_length=255, blank=True, null=True)  # NEW

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img_path = os.path.join(settings.MEDIA_ROOT, self.image.name)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img.save(img_path, optimize=True, quality=70)
