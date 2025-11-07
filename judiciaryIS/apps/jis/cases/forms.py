from django import forms
from .models import Case


class CaseForm(forms.ModelForm):
    hearing_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Case
        fields = [
            "case_number",
            "case_type",
            "plaintiff",
            "defendant",
            "judge",
            "hearing_date",
            "remarks",
        ]
        widgets = {
            "case_number": forms.TextInput(attrs={"placeholder": "e.g. CIV/2025/002"}),
            "plaintiff": forms.TextInput(attrs={"placeholder": "Plaintiff name"}),
            "defendant": forms.TextInput(attrs={"placeholder": "Defendant name"}),
            "judge": forms.TextInput(attrs={"placeholder": "Judge's name"}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
        }
