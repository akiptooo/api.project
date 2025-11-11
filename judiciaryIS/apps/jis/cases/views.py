from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Case
from .forms import CaseForm

def case_list_create(request):
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Case created successfully.")
            return redirect("cases_home")
    else:
        form = CaseForm()

    cases = Case.objects.all().order_by("-id")
    return render(request, "cases/case_list.html", {"form": form, "cases": cases})

def home(request):
    return redirect("cases_home")

def case_create(request):
    return redirect("cases_home")

def case_edit(request, pk):
    return render(request, "cases/case_edit.html", {"pk": pk})

def case_detail(request, pk):
    case = get_object_or_404(Case, pk=pk)
    return render(request, "cases/case_detail.html", {"case": case})

def case_search(request):
    query = request.GET.get("q", "")
    cases = Case.objects.filter(title__icontains=query)
    return render(request, "cases/case_search.html", {"cases": cases, "query": query})
