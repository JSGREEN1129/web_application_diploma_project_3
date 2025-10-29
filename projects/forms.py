from django import forms
from .models import Project

# Form to create or update Project instances


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project  # Link form to Project model
        fields = ['name', 'description', 'start_date', 'end_date', 'status']

        # Customise the HTML widgets for each field
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
