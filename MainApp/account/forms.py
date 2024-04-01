from django import forms
from timesheet.models import TimeSheet,TimeSheetStatus




class TimeSheetStatusUpdateForm(forms.Form):
    
    date = forms.DateField(widget=forms.HiddenInput())
    status = forms.ChoiceField(choices=TimeSheetStatus.choices)