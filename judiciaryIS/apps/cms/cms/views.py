from django.shortcuts import render


def case(request):
    return render(request, "case.html")