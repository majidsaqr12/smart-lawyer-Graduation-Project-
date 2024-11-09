from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    path('', views.home, name='home'),
    path('guide/', views.guide_view, name='guide'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('success/', views.success_view, name='success'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('feature/', views.feature, name='feature'),
    path('team/', views.team, name='team'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('404/', views.custom_404, name='404'),
]
