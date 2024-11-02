from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('lawyer', 'Lawyer'),
        ('person', 'person'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='lawyer')
    
    # Personal Information
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=14, default="+20")
    
    # Account Information
    secret_code = models.CharField(max_length=50)  # Add Secret Code field

    # Extra Info
    verification_code = models.CharField(max_length=6, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_joining = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user.username
