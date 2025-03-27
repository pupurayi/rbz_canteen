# canteen/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import CanteenAttendance, Employee
from datetime import date, timedelta
from django.db.models import Count


@staff_member_required
def dashboard(request):
    # Only show today's attendance
    today_attendance = CanteenAttendance.objects.filter(date=date.today()).select_related(
        'employee', 'employee__user', 'employee__department'
    ).order_by('-time_in')

    context = {
        'today_attendance': today_attendance,
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