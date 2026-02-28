from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from jobs.models import Job
from mocktest.models import TestResult

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get('email', '')
            user.save()
            # The signal will create the profile automatically
            # Let's save the extra fields
            user.profile.qualification = request.POST.get('qualification', '')
            user.profile.phone = request.POST.get('phone', '')
            user.profile.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user_qual = getattr(request.user.profile, 'qualification', '') if hasattr(request.user, 'profile') else ''
    return render(request, 'accounts/dashboard.html', {'user_qual': user_qual})

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    total_users = User.objects.filter(is_superuser=False).count()
    total_jobs = Job.objects.count()
    recent_jobs = Job.objects.order_by('-created_at')[:5]
    recent_results = TestResult.objects.order_by('-date_taken')[:5]
    return render(request, 'accounts/admin_dashboard.html', {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'recent_jobs': recent_jobs,
        'recent_results': recent_results,
    })
