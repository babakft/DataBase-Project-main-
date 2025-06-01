from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from student.models import Student, MaintenanceRequest
from student.forms import StudentRegistrationForm, MaintenanceRequestForm


def home_redirect(request):
    """Redirect to main home page"""
    return redirect('home')


def student_registration(request):
    """Student registration view"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Save student with pending status
            student = form.save(commit=False)
            student.registration_status = 'pending'
            student.save()

            messages.success(
                request,
                'Registration submitted successfully! Your application is pending admin approval.'
            )
            return redirect('student:registration_success')
    else:
        form = StudentRegistrationForm()

    return render(request, 'student/registration_form.html', {'form': form})


def registration_success(request):
    """Registration success page"""
    return render(request, 'student/registration_success.html')


def student_login(request):
    """Student login view"""
    # Check if the user is already logged in
    if 'student_id' in request.session:
        return redirect('student:student_dashboard')

    if request.method == 'POST':
        student_number = request.POST.get('student_number')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        if not student_number or not password:
            messages.error(request, 'Please provide both student number and password.')
            return render(request, 'student/login.html')

        try:
            # Find student by student number
            student = Student.objects.get(student_number=student_number)

            # Check if student is approved
            if student.registration_status != 'approved':
                if student.registration_status == 'pending':
                    messages.error(request, 'Your registration is still pending approval.')
                else:
                    messages.error(request, 'Your registration has been rejected. Please contact administration.')
                return render(request, 'student/login.html')

            # Verify password
            if student.password == password:
                # Create session for student
                request.session['student_id'] = student.id
                request.session['student_name'] = student.student_name
                request.session['student_number'] = student.student_number

                # Set session expiry based on "remember me"
                if remember_me == 'on':
                    request.session.set_expiry(60 * 60 * 24 * 14)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser close

                messages.success(request, f'Welcome back, {student.student_name}!')
                return redirect('student:student_dashboard')
            else:
                messages.error(request, 'Invalid student number or password.')

        except Student.DoesNotExist:
            messages.error(request, 'Invalid student number or password.')

    return render(request, 'student/login.html')


def student_logout(request):
    """Student logout view"""
    # Clear session
    if 'student_id' in request.session:
        del request.session['student_id']
        del request.session['student_name']
        del request.session['student_number']

    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def student_dashboard(request):
    """Student dashboard with their requests and statistics"""
    # Check if student is logged in
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to access your dashboard.')
        return redirect('student:student_login')

    # Get current student
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('student:student_login')

    # Get student's maintenance requests
    requests = MaintenanceRequest.objects.filter(student=student).order_by('-created_at')

    # Calculate statistics
    total_requests = requests.count()
    pending_requests = requests.filter(status='pending').count()
    in_progress_requests = requests.filter(status='in_progress').count()
    completed_requests = requests.filter(status='completed').count()

    # Recent requests (last 5)
    recent_requests = requests[:5]

    context = {
        'student': student,
        'requests': requests,
        'recent_requests': recent_requests,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'in_progress_requests': in_progress_requests,
        'completed_requests': completed_requests,
    }

    return render(request, 'student/dashboard.html', context)


def maintenance_request(request):
    """Create maintenance request"""
    # Check if student is logged in
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to submit a maintenance request.')
        return redirect('student:student_login')

    # Get current student
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('student:student_login')

    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES, student=student)
        if form.is_valid():
            # Save maintenance request
            maintenance_req = form.save(commit=False)
            maintenance_req.student = student
            maintenance_req.status = 'pending'
            maintenance_req.save()

            messages.success(
                request,
                f'Maintenance request submitted successfully! A {maintenance_req.get_service_type_display()} expert will be assigned to handle your request.'
            )
            return redirect('student:request_success')
    else:
        # Pre-fill form with student's location data
        form = MaintenanceRequestForm(student=student)

    return render(request, 'student/maintenance_request.html', {
        'form': form,
        'student': student
    })


def request_success(request):
    """Request success page"""
    # Check if student is logged in
    if 'student_id' not in request.session:
        return redirect('student:student_login')

    return render(request, 'student/request_success.html')


def request_detail(request, request_id):
    """View detailed information about a maintenance request"""
    # Check if student is logged in
    if 'student_id' not in request.session:
        messages.error(request, 'Please log in to view request details.')
        return redirect('student:student_login')

    # Get current student
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        messages.error(request, 'Student not found. Please log in again.')
        return redirect('student:student_login')

    # Get the maintenance request
    maintenance_request = get_object_or_404(
        MaintenanceRequest,
        id=request_id,
        student=student
    )

    context = {
        'request': maintenance_request,
        'student': student,
    }

    return render(request, 'student/request_detail.html', context)


def submit_feedback(request, request_id):
    """Submit feedback and rating for completed request"""
    # Check if student is logged in
    if 'student_id' not in request.session:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    # Get current student
    try:
        student = Student.objects.get(id=request.session['student_id'])
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found'})

    if request.method == 'POST':
        try:
            # Get the maintenance request
            maintenance_request = get_object_or_404(
                MaintenanceRequest,
                id=request_id,
                student=student,
                status='completed'
            )

            rating = int(request.POST.get('rating', 0))
            feedback = request.POST.get('feedback', '').strip()

            # Validate rating
            if not (1 <= rating <= 5):
                return JsonResponse({'success': False, 'error': 'Invalid rating'})

            # Update the request with feedback
            maintenance_request.student_rating = rating
            maintenance_request.student_feedback = feedback
            maintenance_request.save()

            return JsonResponse({
                'success': True,
                'message': 'Thank you for your feedback!'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})