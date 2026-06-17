from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),
    path('mark-read/<int:notif_id>/', views.mark_read, name='notification_mark_read'),
    path('mark-all-read/', views.mark_all_read, name='notification_mark_all_read'),
    path('api/unread-count/', views.unread_count_api, name='notification_unread_count'),
]
