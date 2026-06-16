from django.urls import path
from .views import leave_dashboard, approve_leave

urlpatterns = [
    path('', leave_dashboard, name='leave_dashboard'),
    path('approve/<int:leave_id>/', approve_leave, name='approve_leave'),
]
