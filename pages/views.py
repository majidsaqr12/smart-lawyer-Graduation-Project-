from django.shortcuts import render, redirect
from .models import Offer, Testimonial, FAQCategory, GuideStep
from .forms import ContactForm, AppointmentForm
from django.contrib import messages


def home(request):
    offers = Offer.objects.all()
    testimonials = Testimonial.objects.all()
    testimonials_per_slide = 3
    total_slides = (len(testimonials) + testimonials_per_slide - 1) // testimonials_per_slide
    
    categories = FAQCategory.objects.prefetch_related('faq_set').all() 

    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  

    return render(request, 'pages/home.html', {
        'offers': offers,
        'testimonials': testimonials,
        'total_slides': total_slides,
        'categories': categories, 
        'form': form 
    })

def guide_view(request):
    guide_steps = GuideStep.objects.all().order_by('step_number')
    return render(request, 'pages/guide_page.html', {'guide_steps': guide_steps})


def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('success')
    else:
        form = AppointmentForm()

    return render(request, 'pages/book_appointment.html', {'form': form})


def custom_404(request):
    return render(request, 'pages/404.html', status=404)

def success_view(request):
    return render(request, 'pages/success.html')
