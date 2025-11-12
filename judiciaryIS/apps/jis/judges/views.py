from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cases.models import Case
from registrar.models import CustomUser

@login_required
def judge_dashboard(request):
    """
    Shows the judge's dashboard.
    Lists all cases assigned to this judge.
    """
    # Ensure only judges can access this
    if request.user.role != CustomUser.Role.JUDGE:
        return redirect('dashboard_redirect')
        
    # Get all cases assigned to the current judge
    assigned_cases = Case.objects.filter(
        assigned_judge=request.user
    ).order_by('status', '-date_filed')

    context = {
        'assigned_cases': assigned_cases,
    }
    return render(request, 'judges/dashboard.html', context)

