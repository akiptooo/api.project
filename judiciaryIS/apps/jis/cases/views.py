from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Case, Document, Hearing
from registrar.models import CustomUser

class LawyerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == CustomUser.Role.LAWYER

class CaseListView(LoginRequiredMixin, LawyerRequiredMixin, ListView):
    
    model = Case
    template_name = 'cases/case_list.html'
    context_object_name = 'case_list'

    def get_queryset(self):
        return Case.objects.filter(
            filed_by_lawyer=self.request.user
        ).order_by('-date_filed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cases = self.get_queryset()
        
        # Calculate case statistics
        context['pending_cases'] = cases.filter(status=Case.Status.PENDING).count()
        context['in_progress_cases'] = cases.filter(status=Case.Status.IN_PROGRESS).count()
        context['under_review_cases'] = cases.filter(status=Case.Status.UNDER_REVIEW).count()
        context['closed_cases'] = cases.filter(status=Case.Status.CLOSED).count()
        context['dismissed_cases'] = cases.filter(status=Case.Status.DISMISSED).count()
        
        return context
   
    model = Case
    template_name = 'cases/case_list.html'
    context_object_name = 'case_list'

    def get_queryset(self):
        
        return Case.objects.filter(
            filed_by_lawyer=self.request.user
        ).order_by('-date_filed')

class CaseDetailView(LoginRequiredMixin, DetailView):
  
    model = Case
    template_name = 'cases/case_detail.html'
    context_object_name = 'case'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = self.get_object()
        context['hearings'] = case.hearings.all()
        context['documents'] = case.documents.all()
        return context

    def get(self, request, *args, **kwargs):
        # Security check
        case = self.get_object()
        user = request.user
        
        if user.role == CustomUser.Role.REGISTRAR:
            # Registrar can see all cases
            return super().get(request, *args, **kwargs)
        
        if user.role == CustomUser.Role.LAWYER and case.filed_by_lawyer == user:
            # Lawyer can see their own case
            return super().get(request, *args, **kwargs)
            
        if user.role == CustomUser.Role.JUDGE and case.assigned_judge == user:
            # Judge can see their assigned case
            return super().get(request, *args, **kwargs)

        # If none of the above, deny access
        return redirect('dashboard_redirect') # Or show a 403 page


class CaseCreateView(LoginRequiredMixin, LawyerRequiredMixin, CreateView):
    
    model = Case
    template_name = 'cases/case_form.html'
    fields = ['title', 'description'] # Lawyer only fills these
    success_url = reverse_lazy('cases:case_list')

    def form_valid(self, form):
       
        form.instance.filed_by_lawyer = self.request.user
        
        return super().form_valid(form)
