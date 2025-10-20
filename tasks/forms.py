from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'start_date', 'end_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_end_date(self):
        """Validate end_date is not before start_date or today"""
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        today = timezone.now().date()

        if end_date:
            if end_date < today:
                raise forms.ValidationError("End date cannot be in the past.")

            if start_date and end_date < start_date:
                raise forms.ValidationError(
                    "End date cannot be before start date.")

        return end_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:
            today = timezone.now().date()
            self.initial['start_date'] = today
            self.initial['end_date'] = today + timezone.timedelta(days=7)


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_end_date(self):
        """Validate end_date is not before start_date or today (for active tasks)"""
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        instance = self.instance

        if end_date:
            if start_date and end_date < start_date:
                raise forms.ValidationError(
                    "End date cannot be before start date.")

            today = timezone.now().date()
            if end_date < today and instance.status != 'completed':
                raise forms.ValidationError(
                    "End date cannot be in the past for active tasks.")

        return end_date
