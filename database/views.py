from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from services.models import ServiceExpert
from student.models import MaintenanceRequest, Student


def home(request):
    """Home page view with basic statistics"""
    # Get basic statistics for the home page
    context = {
        'total_experts': ServiceExpert.objects.filter(is_active=True).count(),
        'total_requests': MaintenanceRequest.objects.count(),
        'completed_requests': MaintenanceRequest.objects.filter(status='completed').count(),
        'active_students': Student.objects.filter(registration_status='approved').count(),
    }

    return render(request, 'home.html', context)


def get_experts_api(request):
    """API endpoint to get experts data for the home page"""
    try:
        experts = ServiceExpert.objects.filter(is_active=True).annotate(
            completed_count=Count(
                'assigned_requests',
                filter=Q(assigned_requests__status='completed')
            ),
            avg_rating=Avg('assigned_requests__student_rating')
        )

        experts_data = []
        for expert in experts:
            # Calculate experience years (mock data for now)
            experience_years = min(8, max(2, (timezone.now() - expert.created_at).days // 365 + 2))

            # Get icon based on specialization
            icon_mapping = {
                'electrical': 'fas fa-bolt',
                'plumbing': 'fas fa-faucet',
                'hvac': 'fas fa-wind',
                'carpentry': 'fas fa-hammer',
                'general': 'fas fa-tools',
                'cleaning': 'fas fa-broom',
                'security': 'fas fa-shield-alt',
            }

            expert_data = {
                'id': expert.id,
                'name': expert.expert_name,
                'specialty': expert.get_specialization_display(),
                'specialization_code': expert.specialization,
                'icon': icon_mapping.get(expert.specialization, 'fas fa-tools'),
                'rating': round(expert.avg_rating or 4.5, 1),
                'completed': expert.completed_count,
                'experience': experience_years,
                'phone': expert.phone,
                'email': expert.email,
                'employee_id': expert.employee_id
            }
            experts_data.append(expert_data)

        return JsonResponse({
            'success': True,
            'experts': experts_data,
            'total_count': len(experts_data)
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_services_api(request):
    """API endpoint to get services statistics"""
    try:
        # Get service statistics
        services_stats = []

        # Define service types with their details
        service_types = [
            {
                'code': 'electrical',
                'name': 'برق و روشنایی',
                'icon': 'fas fa-bolt',
                'description': 'تعمیر و نگهداری سیستم‌های برقی، کلیدها، پریزها و تجهیزات روشنایی'
            },
            {
                'code': 'plumbing',
                'name': 'لوله‌کشی و آب',
                'icon': 'fas fa-faucet',
                'description': 'رفع نشتی، تعمیر شیرآلات، رفع گرفتگی و سایر مشکلات لوله‌کشی'
            },
            {
                'code': 'hvac',
                'name': 'تهویه مطبوع',
                'icon': 'fas fa-wind',
                'description': 'تعمیر و سرویس کولرها، سیستم‌های گرمایش و تهویه هوا'
            },
            {
                'code': 'carpentry',
                'name': 'نجاری و تعمیرات',
                'icon': 'fas fa-hammer',
                'description': 'تعمیر درب و پنجره، مبلمان، کابینت و سایر کارهای نجاری'
            },
            {
                'code': 'cleaning',
                'name': 'نظافت و بهداشت',
                'icon': 'fas fa-broom',
                'description': 'خدمات نظافت عمومی، ضدعفونی و مدیریت زباله'
            },
            {
                'code': 'security',
                'name': 'امنیت و نظارت',
                'icon': 'fas fa-shield-alt',
                'description': 'تعمیر سیستم‌های امنیتی، دوربین‌ها و کنترل دسترسی'
            }
        ]

        for service in service_types:
            # Get statistics for this service type
            total_requests = MaintenanceRequest.objects.filter(
                service_type=service['code']
            ).count()

            completed_requests = MaintenanceRequest.objects.filter(
                service_type=service['code'],
                status='completed'
            ).count()

            available_experts = ServiceExpert.objects.filter(
                specialization=service['code'],
                is_active=True
            ).count()

            avg_rating = MaintenanceRequest.objects.filter(
                service_type=service['code'],
                status='completed',
                student_rating__isnull=False
            ).aggregate(avg_rating=Avg('student_rating'))['avg_rating'] or 0

            service_stats = {
                'code': service['code'],
                'name': service['name'],
                'icon': service['icon'],
                'description': service['description'],
                'total_requests': total_requests,
                'completed_requests': completed_requests,
                'available_experts': available_experts,
                'avg_rating': round(avg_rating, 1),
                'completion_rate': round(
                    (completed_requests / total_requests * 100) if total_requests > 0 else 0, 1
                )
            }
            services_stats.append(service_stats)

        return JsonResponse({
            'success': True,
            'services': services_stats
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_stats_api(request):
    """API endpoint to get general statistics for dashboard"""
    try:
        # Current date and time ranges
        now = timezone.now()
        today = now.date()
        this_week_start = today - timedelta(days=today.weekday())
        this_month_start = today.replace(day=1)

        # Basic statistics
        total_students = Student.objects.count()
        approved_students = Student.objects.filter(registration_status='approved').count()
        total_experts = ServiceExpert.objects.filter(is_active=True).count()

        # Request statistics
        total_requests = MaintenanceRequest.objects.count()
        pending_requests = MaintenanceRequest.objects.filter(status='pending').count()
        in_progress_requests = MaintenanceRequest.objects.filter(status='in_progress').count()
        completed_requests = MaintenanceRequest.objects.filter(status='completed').count()

        # Time-based statistics
        today_requests = MaintenanceRequest.objects.filter(
            created_at__date=today
        ).count()

        this_week_requests = MaintenanceRequest.objects.filter(
            created_at__date__gte=this_week_start
        ).count()

        this_month_requests = MaintenanceRequest.objects.filter(
            created_at__date__gte=this_month_start
        ).count()

        # Completion statistics
        avg_rating = MaintenanceRequest.objects.filter(
            status='completed',
            student_rating__isnull=False
        ).aggregate(avg_rating=Avg('student_rating'))['avg_rating'] or 0

        # Response time (average days to complete)
        completed_with_times = MaintenanceRequest.objects.filter(
            status='completed',
            completed_at__isnull=False
        )

        total_response_time = 0
        completed_count = completed_with_times.count()

        if completed_count > 0:
            for request in completed_with_times:
                response_time = (request.completed_at - request.created_at).days
                total_response_time += response_time
            avg_response_time = round(total_response_time / completed_count, 1)
        else:
            avg_response_time = 0

        # Service type distribution
        service_distribution = []
        service_types = MaintenanceRequest.SERVICE_TYPE_CHOICES

        for service_code, service_name in service_types:
            count = MaintenanceRequest.objects.filter(service_type=service_code).count()
            service_distribution.append({
                'service': service_name,
                'count': count,
                'percentage': round((count / total_requests * 100) if total_requests > 0 else 0, 1)
            })

        # Building statistics
        building_stats = MaintenanceRequest.objects.values('building_name').annotate(
            request_count=Count('id')
        ).order_by('-request_count')[:10]

        stats_data = {
            'students': {
                'total': total_students,
                'approved': approved_students,
                'approval_rate': round((approved_students / total_students * 100) if total_students > 0 else 0, 1)
            },
            'experts': {
                'total': total_experts,
                'specializations': ServiceExpert.objects.values('specialization').annotate(
                    count=Count('id')
                ).count()
            },
            'requests': {
                'total': total_requests,
                'pending': pending_requests,
                'in_progress': in_progress_requests,
                'completed': completed_requests,
                'today': today_requests,
                'this_week': this_week_requests,
                'this_month': this_month_requests,
                'completion_rate': round((completed_requests / total_requests * 100) if total_requests > 0 else 0, 1)
            },
            'performance': {
                'avg_rating': round(avg_rating, 1),
                'avg_response_time_days': avg_response_time,
                'total_ratings': MaintenanceRequest.objects.filter(
                    student_rating__isnull=False
                ).count()
            },
            'service_distribution': service_distribution,
            'building_stats': list(building_stats)
        }

        return JsonResponse({
            'success': True,
            'stats': stats_data
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)