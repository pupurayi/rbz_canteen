# canteen/admin.py
from django.contrib import admin
from django import forms
from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .models import Employee, CanteenAttendance, Department
from datetime import datetime


class CanteenAdminSite(admin.AdminSite):
    admin.site. site_header = 'RBZ Canteen Management System'  # Header at top of admin pages
    admin.sitesite_title = 'RBZ Canteen Admin'             # Text in browser title tab
    admin.site.index_title = 'Welcome to the RBZ Attendance Dashboard'  # Text on the admin index page

# Create the custom admin site instance
admin_site = CanteenAdminSite(name='myadmin')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'department')
    search_fields = ('user__first_name', 'user__last_name', 'card_number')
    list_filter = ('department',)


class CanteenAttendanceForm(forms.ModelForm):
    card_number = forms.CharField(
        label='Scan Employee Card',
        required=True,
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'placeholder': 'Tap or enter card number'
        })
    )

    class Meta:
        model = CanteenAttendance
        fields = []

@admin.register(CanteenAttendance)
class CanteenAttendanceAdmin(admin.ModelAdmin):
    form = CanteenAttendanceForm
    list_display = ('employee', 'date', 'time_in')
    list_filter = ('date', 'employee__department')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('get-employee/', self.admin_site.admin_view(self.get_employee), name='get_employee'),
        ]
        return custom_urls + urls

    def get_employee(self, request):
        card_number = request.GET.get('card_number')
        try:
            employee = Employee.objects.get(card_number=card_number)
            data = {
                'exists': True,
                'name': employee.user.get_full_name(),
                'department': str(employee.department),
            }
        except Employee.DoesNotExist:
            data = {'exists': False}
        return JsonResponse(data)

    def save_model(self, request, obj, form, change):
        card_number = form.cleaned_data['card_number']
        try:
            employee = Employee.objects.get(card_number=card_number)
            obj.employee = employee

            if CanteenAttendance.objects.filter(employee=employee, date=datetime.now().date()).exists():
                messages.warning(request, f"{employee.user.get_full_name()} already had lunch today!")
            else:
                messages.success(request, f"Attendance recorded for {employee.user.get_full_name()}")

            super().save_model(request, obj, form, change)
        except Employee.DoesNotExist:
            messages.error(request, "Employee not found with this card number")
            return

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        if 'adminform' in context and 'employee' in context['adminform'].form.fields:
            del context['adminform'].form.fields['employee']
        return super().render_change_form(request, context, add, change, form_url, obj)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)