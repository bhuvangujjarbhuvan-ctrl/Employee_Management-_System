"""
URL configuration for Company project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Employee.views import custom_logout

urlpatterns = [
    path('admin/logout/', custom_logout),
    path('admin/', admin.site.urls),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('Company.api_urls')),
    path('leave/', include('Leave.urls')),
    path('projects/', include('Projects.urls')),
    path('payroll/', include('Payroll.urls')),
    path('notifications/', include('Notifications.urls')),
    path('', include("Employee.urls")),
    path('', include("Departments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
