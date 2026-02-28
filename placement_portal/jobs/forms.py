from django import forms
from django.core.exceptions import ValidationError

def validate_csv(value):
    if not value.name.endswith('.csv'):
        raise ValidationError('Only CSV files are allowed.')

class JobCSVUploadForm(forms.Form):
    csv_file = forms.FileField(validators=[validate_csv])
