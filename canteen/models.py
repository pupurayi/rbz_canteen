# canteen/models.py
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} (Card: {self.card_number})"


class CanteenAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'date')
        verbose_name_plural = "Canteen Attendances"

    def __str__(self):
        return f"{self.employee} - {self.date}"