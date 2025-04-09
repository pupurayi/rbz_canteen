import datetime

from django import forms
from .models import Employee, CanteenAttendance

class CardTapForm(forms.Form):
    card_number = forms.CharField(max_length=50, label='Scan Your Access Card')

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search employees or departments')