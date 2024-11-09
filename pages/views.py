from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def home(request):
    return render(request, 'pages/home.html')

def custom_404(request):
    return render(request, 'pages/404.html', status=404)

def success_view(request):
    return render(request, 'pages/success.html')

def about(request):
    return render(request, 'pages/about.html')

def service(request):
    return render(request, 'pages/service.html')

def feature(request):
    return render(request, 'pages/feature.html')

def team(request):
    return render(request, 'pages/team.html')

def faq(request):
    return render(request, 'pages/faq.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save data to the database
            return redirect('success')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})
