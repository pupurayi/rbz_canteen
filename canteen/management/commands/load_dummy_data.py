# canteen/management/commands/load_dummy_data.py
from django.db.utils import IntegrityError

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from canteen.models import Department, Employee, CanteenAttendance
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Loads dummy data for RBZ Canteen system'

    def handle(self, *args, **options):
        # Create departments
        departments = [
            'Finance',
            'Human Resources',
            'IT',
            'Operations',
            'Risk Management',
        ]

        dept_objs = []
        for dept in departments:
            d, created = Department.objects.get_or_create(name=dept)
            dept_objs.append(d)
            self.stdout.write(self.style.SUCCESS(f'Created department: {dept}'))

        # Create 50 dummy employees
        first_names = ['John', 'Jane', 'Robert', 'Mary', 'David', 'Sarah', 'Michael', 'Emily', 'James', 'Jennifer']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez',
                      'Wilson']

        for i in range(1, 51):
            first = random.choice(first_names)
            last = random.choice(last_names)
            username = f"{first.lower()}{last.lower()}"
            email = f"{username}@rbz.co.zw"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': email,
                }
            )

            if created:
                user.set_password('password123')
                user.save()

            card_number = f"RBZ-{1000 + i}"
            employee, emp_created = Employee.objects.get_or_create(
                user=user,
                defaults={
                    'card_number': card_number,
                    'department': random.choice(dept_objs),
                }
            )

            self.stdout.write(self.style.SUCCESS(f'Created employee: {first} {last} ({card_number})'))

            # Create attendance records for the last 30 days (random)
            for day in range(30):
                if random.random() > 0.7:  # 30% chance of attending on any given day
                    att_date = date.today() - timedelta(days=30 - day)
                    try:
                        CanteenAttendance.objects.create(
                            employee=employee,
                            date=att_date
                        )
                    except IntegrityError:
                        # Skip if attendance already exists for this employee on this date
                        continue

        self.stdout.write(self.style.SUCCESS('Successfully loaded dummy data'))