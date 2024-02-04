from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='uploads/profile_images/', null=True, blank=True)
