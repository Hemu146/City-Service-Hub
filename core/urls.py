# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('forget/', views.forget_view, name='forget'),
    path('services/', views.service_view, name='services'),
    path('service-provider/', views.service_provider_view, name='service_provider'),
    path('user-dashboard/', views.user_dashboard_view, name='user_dashboard'),
    path('user-profile/update/', views.update_user_profile, name='update_user_profile'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path("add-service/", views.add_service, name="add_service"),
    path("edit-service/<int:id>/", views.edit_service, name="edit_service"),
    path("delete-service/<int:id>/", views.delete_service, name="delete_service"),
    path("update-profile/", views.update_provider_profile, name="update_profile"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("approve-service/<int:id>/", views.approve_service, name="approve_service"),
    path("toggle-favorite/<int:service_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("book-service/<int:service_id>/", views.book_service, name="book_service"),
    path("booking/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
    path("booking/<int:booking_id>/update-status/", views.update_booking_status, name="update_booking_status"),
]