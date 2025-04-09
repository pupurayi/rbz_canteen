# canteen/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.generic.dates import timezone_today

from .models import CanteenAttendance, Employee, Department
from datetime import date, timedelta
from django.db.models import Count


@staff_member_required
def dashboard(request):
    departments = Department.objects.all()

    # Only show today's attendance
    today_attendance = CanteenAttendance.objects.filter(date=date.today()).select_related(
        'employee', 'employee__user', 'employee__department'
    ).order_by('-time_in')

    context = {
        'today_attendance': today_attendance,
    }

    # Get selected department from filter
    selected_department = request.GET.get('department')
    if selected_department:
        today_attendance = today_attendance.filter(employee__department__id=selected_department)

    context = {
        'departments': departments,
        'today_attendance': today_attendance,
        'selected_department': selected_department,
    }
    return render(request, 'canteen/dashboard.html', context)


@staff_member_required
def reports(request):
    # Get attendance for last 30 days
    start_date = date.today() - timedelta(days=30)
    daily_attendance = CanteenAttendance.objects.filter(
        date__gte=start_date
    ).values('date').annotate(
        total=Count('id')
    ).order_by('date')

    # Department breakdown
    dept_breakdown = CanteenAttendance.objects.filter(
        date__gte=start_date
    ).values('employee__department__name').annotate(
        total=Count('id')
    ).order_by('-total')

    context = {
        'daily_attendance': daily_attendance,
        'dept_breakdown': dept_breakdown,
    }
    return render(request, 'canteen/reports.html', context)