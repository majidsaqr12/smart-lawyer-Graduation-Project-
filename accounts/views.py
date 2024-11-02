from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from .forms import  PersonalInfoForm, SchoolInfoForm, AccountInfoForm, PasswordResetVerificationForm, PasswordResetForm, UserTypeForm, PasswordResetRequestForm
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
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def multi_step_register(request):
    step = request.GET.get('step', '1')  # Default to step 1
    
    # Handle POST request
    if request.method == 'POST':
        if 'previous' in request.POST:  # Handle Previous button click
            if step == '2':
                return redirect(f"{reverse('register')}?step=1")
            elif step == '3':
                return redirect(f"{reverse('register')}?step=2")
            elif step == '4':
                return redirect(f"{reverse('register')}?step=3")
        
        # Handle Next button click
        if step == '1':
            form = UserTypeForm(request.POST)
            if form.is_valid():
                request.session['user_type_info'] = form.cleaned_data  # Save data in session
                return redirect(f"{reverse('register')}?step=2")
        elif step == '2':
            form = SchoolInfoForm(request.POST)
            if form.is_valid():
                request.session['school_info'] = form.cleaned_data  # Save data in session
                return redirect(f"{reverse('register')}?step=3")
        elif step == '3':
            form = PersonalInfoForm(request.POST)
            if form.is_valid():
                personal_info = form.cleaned_data
                # Convert date to string before saving in session
                personal_info['date_of_birth'] = personal_info['date_of_birth'].strftime('%Y-%m-%d')
                request.session['personal_info'] = personal_info  # Save the form data with string date, including username
                return redirect(f"{reverse('register')}?step=4")
        elif step == '4':
            form = AccountInfoForm(request.POST)
            if form.is_valid():
                user_type_info = request.session.get('user_type_info')
                school_info = request.session.get('school_info')
                personal_info = request.session.get('personal_info')

                # Convert date_of_birth back to date object
                personal_info['date_of_birth'] = datetime.strptime(personal_info['date_of_birth'], '%Y-%m-%d').date()

                # Create the user and profile
                user = form.save(commit=False)

                # Set the username from session data saved in step 3
                user.username = personal_info['username']  # Get the username from session

                user.is_active = False  # Set to inactive until email verification
                user.save()

                # Create profile with the additional details
                profile = Profile.objects.create(
                    user=user,
                    user_type=user_type_info['user_type'],
                    country=school_info['country'],
                    education_system=school_info['education_system'],
                    grade=school_info['grade'],
                    first_name=personal_info['first_name'],
                    last_name=personal_info['last_name'],
                    full_name=f"{personal_info['first_name']} {personal_info['last_name']}",
                    gender=personal_info['gender'],
                    date_of_birth=personal_info['date_of_birth'],
                    phone_number=personal_info['phone_number'],
                    secret_code=form.cleaned_data['secret_code'],
                )
                profile.verification_code = generate_code()  # Generate a 6-character code
                profile.save()

                # Send the verification email
                send_verification_email(user, profile.verification_code)

                # Notify the user to verify their email
                messages.success(request, 'Registration successful. Please verify your email.')
                return redirect('verify_email', user_id=user.id)

    # Handle GET request (when navigating back to a step)
    else:
        if step == '1':
            form = UserTypeForm(initial=request.session.get('user_type_info'))  # Load previous data
        elif step == '2':
            form = SchoolInfoForm(initial=request.session.get('school_info'))  # Load previous data
        elif step == '3':
            form = PersonalInfoForm(initial=request.session.get('personal_info'))  # Load previous data
        else:
            form = AccountInfoForm()

    return render(request, 'accounts/signup.html', {'form': form, 'step': step})


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
    return render(request, 'accounts/profile.html', {'user': request.user})