from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import login, authenticate, logout  
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin

# Import your models and forms
from cases.models import Case
from .models import CustomUser
from .forms import UserSignUpForm  

class RegistrarRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure user is a registrar"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == CustomUser.Role.REGISTRAR
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to access this page.")
        return redirect('/registrar/login/')

def register(request):
    if request.method == 'POST':
        print("=== REGISTRATION DEBUG ===")
        form = UserSignUpForm(request.POST)  
        print(f"Form valid: {form.is_valid()}")
        
        if form.is_valid():
            user = form.save()
            print(f"User created: {user.username}, Active: {user.is_active}, Role: {user.role}")
            login(request, user)
            print(f"User logged in: {request.user.is_authenticated}")
            messages.success(request, f"Registration successful! Welcome {user.username}!")
            
            # Redirect based on user role
            return redirect('dashboard_redirect')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserSignUpForm()  
    
    return render(request, 'registrar/register.html', {'form': form})

@login_required
def dashboard_redirect(request):
    print(f"Dashboard redirect - User: {request.user}, Role: {request.user.role}")
    
    if not hasattr(request.user, 'role') or not request.user.role:
        messages.error(request, "Your account doesn't have a valid role assigned.")
        return redirect('/registrar/login/')
    
    try:
        if request.user.role == CustomUser.Role.REGISTRAR:
            return redirect('/registrar/dashboard/')
        elif request.user.role == CustomUser.Role.JUDGE:
            return redirect('/judges/dashboard/')
        elif request.user.role == CustomUser.Role.LAWYER:
            return redirect('/cases/')  
        else:
            messages.warning(request, "No specific dashboard found for your role.")
            return redirect('/admin/')
    except Exception as e:
        print(f"Redirect error: {e}")
        # Fallback to a safe page
        return redirect('/registrar/')

def manual_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Login attempt: {username}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(f"Login SUCCESS: {user.username}, Role: {user.role}")
            messages.success(request, f"Welcome back, {user.username}!")
            
            # Handle 'next' parameter for redirects
            next_url = request.GET.get('next', '/registrar/')
            return redirect(next_url)
        else:
            print("Login FAILED")
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'registrar/login.html')

@login_required
def registrar_dashboard(request):
    """
    Shows the registrar's dashboard.
    The main job is to view and assign cases.
    """
    
    if request.user.role != CustomUser.Role.REGISTRAR:
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    # Get cases that are pending and have no judge assigned
    unassigned_cases = Case.objects.filter(
        status=Case.Status.PENDING,
        assigned_judge__isnull=True
    ).order_by('date_filed')
    
    # Get all judges for the assignment dropdown
    judges = CustomUser.objects.filter(role=CustomUser.Role.JUDGE)
    
    context = {
        'unassigned_cases': unassigned_cases,
        'judges': judges,
        'user': request.user
    }
    return render(request, 'registrar/dashboard.html', context)

@login_required
def assign_case_to_judge(request, case_id):
    if request.user.role != CustomUser.Role.REGISTRAR:
        return HttpResponseForbidden("Access denied.")

    if request.method == 'POST':
        case = get_object_or_404(Case, id=case_id)
        judge_id = request.POST.get('judge_id')

        if judge_id:
            judge = get_object_or_404(CustomUser, id=judge_id, role=CustomUser.Role.JUDGE)
            case.assigned_judge = judge
            case.status = Case.Status.IN_PROGRESS  # Update status
            case.save()
            messages.success(request, f"Case assigned to {judge.get_full_name()}.")
        else:
            messages.error(request, "Please select a judge.")

    return redirect('/registrar/dashboard/')

# Custom Login View (alternative to manual_login)
class CustomLoginView(LoginView):
    template_name = 'registrar/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard_redirect')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

# Custom logout view (if you prefer GET requests)
def custom_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('/registrar/login/')

# Debug and test views
def debug_auth(request):
    """Debug view to check authentication status"""
    return HttpResponse(f"""
        <h1>Auth Debug</h1>
        <p>User: {request.user}</p>
        <p>Authenticated: {request.user.is_authenticated}</p>
        <p>Role: {getattr(request.user, 'role', 'No role')}</p>
        <p>Session key: {request.session.session_key}</p>
        <hr>
        <a href="/registrar/login/">Login</a> | 
        <a href="/registrar/register/">Register</a> |
        <a href="/registrar/dashboard/">Dashboard</a> |
        <a href="/registrar/logout/">Logout</a>
    """)

def test_page(request):
    """Simple test page to check if views are working"""
    return HttpResponse("""
        <h1>Test Page - Working!</h1>
        <p>If you can see this, the views are working.</p>
        <ul>
            <li><a href="/registrar/login/">Login</a></li>
            <li><a href="/registrar/register/">Register</a></li>
            <li><a href="/registrar/dashboard/">Dashboard</a></li>
            <li><a href="/registrar/debug-auth/">Debug Auth</a></li>
        </ul>
    """)

def home(request):
    """Home page with role-based content"""
    context = {}
    
    if request.user.is_authenticated:
        # Add user-specific context for logged-in users
        context['user_role'] = request.user.role
        context['user_name'] = request.user.get_full_name() or request.user.username
    
    return render(request, 'registrar/home.html', context)

def welcome(request):
    """Welcome page for newly registered users"""
    if not request.user.is_authenticated:
        return redirect('/registrar/login/')
    
    return render(request, 'registrar/welcome.html', {
        'user': request.user
    })

# Template debug view
def debug_templates(request):
    """Debug view to check template loading"""
    from django.template.loader import get_template
    
    templates_to_check = [
        'base.html',
        'registrar/base.html', 
        'registrar/login.html',
        'registrar/register.html',
        'registrar/dashboard.html',
        'cases/case_list.html',
    ]
    
    results = []
    for template_name in templates_to_check:
        try:
            template = get_template(template_name)
            results.append(f"✅ {template_name} - FOUND")
        except:
            results.append(f"❌ {template_name} - NOT FOUND")
    
    return HttpResponse("<br>".join(results))

# URL debug view
def debug_urls(request):
    """Debug view to see all available URLs"""
    from django.urls import get_resolver
    
    resolver = get_resolver()
    url_list = []
    
    def extract_urls(urlpatterns, prefix=''):
        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                # Include pattern
                extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            else:
                # Regular pattern
                url_info = f"{prefix + str(pattern.pattern)} -> {getattr(pattern, 'name', 'No name')}"
                url_list.append(url_info)
    
    extract_urls(resolver.url_patterns)
    
    html = "<h1>All URL Patterns</h1><ul>"
    for url in sorted(url_list):
        html += f"<li>{url}</li>"
    html += "</ul>"
    
    return HttpResponse(html)

def registrar_required(function=None):
    """Decorator to ensure user is a registrar"""
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.role == CustomUser.Role.REGISTRAR,
        login_url='/registrar/login/'
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@registrar_required
def user_management(request):
    """User management dashboard for registrars"""
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Get statistics
    total_users = users.count()
    lawyers = users.filter(role=CustomUser.Role.LAWYER).count()
    judges = users.filter(role=CustomUser.Role.JUDGE).count()
    registrars = users.filter(role=CustomUser.Role.REGISTRAR).count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'lawyers_count': lawyers,
        'judges_count': judges,
        'registrars_count': registrars,
    }
    return render(request, 'registrar/user_management.html', context)

class UserUpdateView(RegistrarRequiredMixin, UpdateView):
    """View for registrars to edit user information"""
    model = CustomUser
    template_name = 'registrar/user_edit.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    success_url = reverse_lazy('user_management')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['editing_user'] = self.get_object()
        return context

class UserDeleteView(RegistrarRequiredMixin, DeleteView):
    """View for registrars to delete users"""
    model = CustomUser
    template_name = 'registrar/user_confirm_delete.html'
    success_url = reverse_lazy('user_management')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deleting_user'] = self.get_object()
        return context

@registrar_required
def toggle_user_status(request, user_id):
    """Quick toggle for user active status"""
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_active = not user.is_active
        user.save()
        
        action = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User {user.username} has been {action}.")
    
    return redirect('user_management')