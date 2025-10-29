from django import forms
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'start_date', 'end_date', 'status']
        widgets = {
            # Date input widget with minimum date set to today
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
                # Prevent selecting past dates
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
                # Prevent selecting past dates
            }),
            # Styling the input fields with Bootstrap classes
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea
            (attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_end_date(self):
        """
        Custom validation for the end_date field:
        - end_date cannot be in the past
        - end_date cannot be before start_date
        """
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
        """
        Override form initialization to set default start_date and end_date
        for new instances (i.e., when creating a new task).
        """
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:
            today = timezone.now().date()
            self.initial['start_date'] = today
            self.initial['end_date'] = today + timezone.timedelta(days=7)


class TaskEditForm(forms.ModelForm):
    """
    Form used for editing existing tasks.
    Excludes 'status' field as editing status might be handled separately.
    """
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
            'description': forms.Textarea
            (attrs={'class': 'form-control', 'rows': 5}),
        }

    def clean_end_date(self):
        """
        Custom validation for end_date during task edit:
        - end_date cannot be before start_date
        - end_date cannot be in the past if
        the task is still active (i.e., not completed)
        """
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        instance = self.instance

        if end_date:
            if start_date and end_date < start_date:
                raise forms.ValidationError(
                    "End date cannot be before start date.")

            today = timezone.now().date()
            # For active tasks, end_date cannot be in the past
            if end_date < today and instance.status != 'completed':
                raise forms.ValidationError(
                    "End date cannot be in the past for active tasks.")

        return end_date
