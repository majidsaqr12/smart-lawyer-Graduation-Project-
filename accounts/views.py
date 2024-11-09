from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .forms import  UserRegisterForm, PasswordResetVerificationForm, PasswordResetForm, PasswordResetRequestForm
from .models import Profile
import random
import string
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.urls import reverse


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AuthenticationForm()
    return render(request, 'base.html', {'form': form})


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            login(request, user)
            return redirect('home')
    else:
        user_form = UserRegisterForm()

    return render(request, 'base.html', {'user_form': user_form})


def send_verification_email(user, verification_code):
    """Function to send email verification"""
    subject = 'Verify your email'
    message = f'Your verification code is: {verification_code}'
    from_email = 'from@example.com'  # Replace with your email sender
    recipient_list = [user.email]
    
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Error sending email: {str(e)}")



def verify_email(request, user_id):
    try:
        # Fetch the profile associated with the user
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('login')

    if request.method == 'POST':
        # Handle 'Resend Code' button click
        if 'resend_code' in request.POST:
            # Generate a new verification code
            profile.verification_code = generate_code()
            profile.save()  # Save the new code in the database
            
            # Send the new code to the user's email
            send_verification_email(profile.user, profile.verification_code)
            messages.success(request, 'A new verification code has been sent to your email.')
            return redirect('verify_email', user_id=user_id)
        
        # Handle 'Verify' button click
        if 'verify' in request.POST:
            code = request.POST.get('code')
            if profile.verification_code == code:
                # Activate the user account after successful verification
                user = profile.user
                user.is_active = True
                user.save()

                # Clear the verification code after successful activation
                profile.verification_code = ''
                profile.save()
                
                messages.success(request, 'Email verified successfully. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid verification code.')

    return render(request, 'accounts/verify_email.html', {'user_id': user_id})


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                profile = Profile.objects.get(user=user)
                
                # Generate a verification code
                verification_code = get_random_string(length=6, allowed_chars='0123456789')
                profile.verification_code = verification_code
                profile.save()

                # Send verification code via email
                send_mail(
                    'Password Reset Verification Code',
                    f'Your verification code is: {verification_code}',
                    'from@example.com',  # Change this to your email sender
                    [email],
                    fail_silently=False,
                )

                messages.success(request, 'Verification code sent to your email.')
                return redirect('password_reset_verify', user_id=user.id)

            except User.DoesNotExist:
                messages.error(request, 'No user with that email exists.')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset_request.html', {'form': form})



def password_reset_verify(request, user_id):
    if request.method == 'POST':
        form = PasswordResetVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                profile = Profile.objects.get(user_id=user_id)
                if profile.verification_code == code:
                    # Redirect to password reset form
                    return redirect('password_reset_form', user_id=user_id)
                else:
                    messages.error(request, 'Invalid verification code.')
            except Profile.DoesNotExist:
                messages.error(request, 'User profile not found.')

    form = PasswordResetVerificationForm()
    return render(request, 'accounts/password_reset_verify.html', {'form': form})



def password_reset_form(request, user_id):
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = PasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been reset successfully. You can now login.')
            return redirect('login')

    else:
        form = PasswordResetForm(user)

    return render(request, 'accounts/password_reset_form.html', {'form': form})



@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/index.html', {'user': request.user, 'profile': profile})