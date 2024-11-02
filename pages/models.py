from django.db import models
from django.utils import timezone


class Offer(models.Model):
    CATEGORY_CHOICES = [
        ('Primary', 'Primary'),
        ('Middle School', 'Middle School'),
        ('High School', 'High School')
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    quarterly_price = models.DecimalField(max_digits=10, decimal_places=2)
    annually_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='TND')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.category

class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    video = models.FileField(upload_to='videos/', default='videos/default.mp4')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name


class FAQCategory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question
    
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    complaint_type = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name
    

class GuideStep(models.Model):
    step_number = models.IntegerField()
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/guide', default='videos/default.mp4')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.step_number} - {self.title}"

class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.appointment_date}"