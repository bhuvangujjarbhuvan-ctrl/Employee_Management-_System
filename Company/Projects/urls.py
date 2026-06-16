from django.urls import path
from .views import projects_dashboard

urlpatterns = [
    path('', projects_dashboard, name='projects_dashboard'),
]
