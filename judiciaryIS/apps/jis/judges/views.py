from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Judge
from .forms import JudgeForm

def judge_edit(request, pk):
    return render(request, "judges/judge_edit.html", {"pk": pk})


def judges_list_create(request):
    if request.method == "POST":
        form = JudgeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Judge added.")
            return redirect("judges")
    else:
        form = JudgeForm()

    judges = Judge.objects.all().order_by("last_name")

    return render(request, "judges/judges_list.html", {
        "form": form,
        "judges": judges,
    })
