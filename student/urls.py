from django.urls import path
from student.views import (
    student_registration,
    registration_success,
    student_login,
    student_logout,
    student_dashboard,
    maintenance_request,
    request_success,
    request_detail,
    submit_feedback,
    home_redirect
)

app_name = 'student'

urlpatterns = [
    # Home redirect
    path('', home_redirect, name='home'),

    # Authentication
    path('register/', student_registration, name='student_registration'),
    path('registration-success/', registration_success, name='registration_success'),
    path('login/', student_login, name='student_login'),
    path('logout/', student_logout, name='student_logout'),

    # Dashboard
    path('dashboard/', student_dashboard, name='student_dashboard'),

    # Maintenance Requests
    path('maintenance/', maintenance_request, name='maintenance_request'),
    path('request-success/', request_success, name='request_success'),
    path('request/<int:request_id>/', request_detail, name='request_detail'),

    # Feedback
    path('feedback/<int:request_id>/', submit_feedback, name='submit_feedback'),
]