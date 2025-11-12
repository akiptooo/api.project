from django import forms
from .models import Judge

class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ['first_name', 'last_name', 'position', 'email']
