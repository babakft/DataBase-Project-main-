from django.core.management.base import BaseCommand
from django.utils import timezone
from services.models import ServiceExpert
from student.models import Student, MaintenanceRequest
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate the database with initial data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--experts',
            type=int,
            default=10,
            help='Number of experts to create',
        )
        parser.add_argument(
            '--students',
            type=int,
            default=20,
            help='Number of students to create',
        )
        parser.add_argument(
            '--requests',
            type=int,
            default=50,
            help='Number of maintenance requests to create',
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')

        # Create experts
        self.create_experts(options['experts'])

        # Create students
        self.create_students(options['students'])

        # Create maintenance requests
        self.create_requests(options['requests'])

        self.stdout.write(
            self.style.SUCCESS('Successfully populated initial data!')
        )

    def create_experts(self, count):
        self.stdout.write(f'Creating {count} experts...')

        expert_names = [
            'احمد محمدی', 'فاطمه احمدی', 'علی رضایی', 'مریم کریمی',
            'حسن موسوی', 'سارا نوری', 'محمد صادقی', 'زهرا حسینی',
            'رضا قاسمی', 'طاهره امینی', 'مجید فرهادی', 'لیلا شریفی',
            'کامیار جعفری', 'نسرین خانی', 'بهروز ملکی'
        ]

        specializations = [
            'electrical', 'plumbing', 'hvac', 'carpentry',
            'general', 'cleaning', 'security'
        ]

        for i in range(count):
            if i < len(expert_names):
                name = expert_names[i]
            else:
                name = f'کارشناس {i + 1}'

            expert = ServiceExpert.objects.create(
                expert_name=name,
                employee_id=f'EXP{1000 + i}',
                password='password123',  # In production, use proper password hashing
                specialization=random.choice(specializations),
                phone=f'0913{random.randint(1000000, 9999999)}',
                email=f'expert{i + 1}@university.ac.ir',
                is_active=True
            )

        self.stdout.write(f'Created {count} experts successfully.')

    def create_students(self, count):
        self.stdout.write(f'Creating {count} students...')

        student_names = [
            'علی احمدی', 'فاطمه رضایی', 'محمد کریمی', 'مریم موسوی',
            'حسین نوری', 'زهرا صادقی', 'رضا حسینی', 'طاهره قاسمی',
            'مجید امینی', 'لیلا فرهادی', 'کامیار شریفی', 'نسرین جعفری',
            'بهروز خانی', 'سارا ملکی', 'احمد نظری', 'فرشته باقری',
            'محسن تقوی', 'مهناز کاظمی', 'سعید رحمانی', 'شیدا محمودی'
        ]

        buildings = ['خوابگاه شهید بهشتی', 'خوابگاه شهید چمران', 'خوابگاه فردوسی', 'خوابگاه حافظ']

        for i in range(count):
            if i < len(student_names):
                name = student_names[i]
            else:
                name = f'دانشجو {i + 1}'

            student = Student.objects.create(
                student_name=name,
                email=f'student{i + 1}@student.university.ac.ir',
                student_number=f'{98000000 + i}',
                password='password123',  # In production, use proper password hashing
                room_number=f'{random.randint(101, 499)}',
                building_name=random.choice(buildings),
                floor_number=random.randint(1, 4),
                registration_status='approved'
            )

        self.stdout.write(f'Created {count} students successfully.')

    def create_requests(self, count):
        self.stdout.write(f'Creating {count} maintenance requests...')

        students = list(Student.objects.all())
        experts = list(ServiceExpert.objects.all())

        if not students:
            self.stdout.write(self.style.ERROR('No students found. Create students first.'))
            return

        request_titles = [
            'مشکل در برق اتاق',
            'نشتی شیر آب',
            'خرابی کولر',
            'شکستگی در درب کمد',
            'مشکل در روشنایی راهرو',
            'گرفتگی فاضلاب',
            'خرابی پریز برق',
            'مشکل در قفل درب',
            'نیاز به تعمیر پنجره',
            'خرابی لامپ سقفی'
        ]

        descriptions = [
            'لطفاً مشکل موجود را در اسرع وقت برطرف کنید.',
            'این مشکل باعث ایجاد مزاحمت می‌شود.',
            'نیاز به تعمیر فوری دارد.',
            'مشکل از چند روز پیش شروع شده است.',
            'لطفاً کارشناس مربوطه را اعزام کنید.'
        ]

        service_types = ['electrical', 'plumbing', 'hvac', 'carpentry', 'general', 'cleaning', 'security']
        statuses = ['pending', 'approved', 'in_progress', 'completed']

        for i in range(count):
            student = random.choice(students)
            status = random.choice(statuses)
            service_type = random.choice(service_types)

            # Create request
            created_time = timezone.now() - timedelta(days=random.randint(1, 30))

            request = MaintenanceRequest.objects.create(
                student=student,
                title=random.choice(request_titles),
                description=random.choice(descriptions),
                service_type=service_type,
                room_number=student.room_number,
                building_name=student.building_name,
                floor_number=student.floor_number,
                status=status,
                created_at=created_time
            )

            # If request is not pending, assign expert and set dates
            if status != 'pending':
                # Find expert with matching specialization
                matching_experts = [e for e in experts if e.specialization == service_type]
                if matching_experts:
                    expert = random.choice(matching_experts)
                else:
                    expert = random.choice(experts)

                request.assigned_expert = expert
                request.assigned_at = created_time + timedelta(hours=random.randint(1, 24))

                if status in ['in_progress', 'completed']:
                    request.work_started_at = request.assigned_at + timedelta(hours=random.randint(1, 48))
                    request.expert_notes = 'کار شروع شده است.'

                    if status == 'completed':
                        request.completed_at = request.work_started_at + timedelta(hours=random.randint(1, 72))
                        request.completed_by = expert.expert_name
                        request.completion_notes = 'کار با موفقیت تکمیل شد.'
                        request.student_rating = random.randint(3, 5)
                        if random.choice([True, False]):
                            request.student_feedback = 'خدمات ارائه شده رضایت‌بخش بود.'

                request.save()

        self.stdout.write(f'Created {count} maintenance requests successfully.')

    def create_admin_user(self):
        """Create a superuser for admin access"""
        from django.contrib.auth.models import User

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@university.ac.ir',
                password='admin123'
            )
            self.stdout.write('Created admin user (username: admin, password: admin123)')
        else:
            self.stdout.write('Admin user already exists.')