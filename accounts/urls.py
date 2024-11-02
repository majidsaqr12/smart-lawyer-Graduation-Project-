from django.urls import path
from .views import user_login, multi_step_register, profile_view, verify_email, password_reset_request, password_reset_verify, password_reset_form
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', multi_step_register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('verify_email/<int:user_id>/', verify_email, name='verify_email'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset_verify/<int:user_id>/', password_reset_verify, name='password_reset_verify'),
    path('password_reset_form/<int:user_id>/', password_reset_form, name='password_reset_form'),
]
