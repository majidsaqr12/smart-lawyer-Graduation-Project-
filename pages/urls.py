from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
    path('', views.home, name='home'),
    path('guide/', views.guide_view, name='guide'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('success/', views.success_view, name='success'),
]
