from django.shortcuts import render
from django import forms
from .models import Case


def home(request):
    return render(request, "home.html")

def case_search(request):
    return render(request, 'case_search.html')

def e_filing(request):
    return render(request, 'e_filing.html')

def calendar_view(request):
    return render(request, 'calendar.html')

def directory(request):
    return render(request, 'directory.html')

def dashboard(request):
    return render(request, 'dashboard.html')


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
