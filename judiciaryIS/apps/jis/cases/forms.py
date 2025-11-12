from django import forms
from .models import Case, Hearing, Document

class CaseCreateForm(forms.ModelForm):
    """Form for a lawyer to create a new case."""
    class Meta:
        model = Case
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }

class CaseStatusUpdateForm(forms.ModelForm):
    """Form for a Judge or Registrar to update the case status."""
    class Meta:
        model = Case
        fields = ['status']

class HearingCreateForm(forms.ModelForm):
    """Form for a Judge or Registrar to schedule a hearing."""
    class Meta:
        model = Hearing
        fields = ['hearing_date', 'location', 'notes']
        widgets = {
            'hearing_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    
    # This is necessary to make the HTML5 widget work with Django
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'hearing_date' in self.fields:
            self.fields['hearing_date'].input_formats = ('%Y-%m-%dT%H:%M',)

class DocumentUploadForm(forms.ModelForm):
    """Form for any authenticated user to upload a document to a case."""
    class Meta:
        model = Document
        fields = ['description', 'file']from django import forms
from .models import Case, Hearing, Document

class CaseCreateForm(forms.ModelForm):
    """Form for a lawyer to create a new case."""
    class Meta:
        model = Case
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }

class CaseStatusUpdateForm(forms.ModelForm):
    """Form for a Judge or Registrar to update the case status."""
    class Meta:
        model = Case
        fields = ['status']

class HearingCreateForm(forms.ModelForm):
    """Form for a Judge or Registrar to schedule a hearing."""
    class Meta:
        model = Hearing
        fields = ['hearing_date', 'location', 'notes']
        widgets = {
            'hearing_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'hearing_date' in self.fields:
            self.fields['hearing_date'].input_formats = ('%Y-%m-%dT%H:%M',)

class DocumentUploadForm(forms.ModelForm):
    """Form for any authenticated user to upload a document to a case."""
    class Meta:
        model = Document
        fields = ['description', 'file']