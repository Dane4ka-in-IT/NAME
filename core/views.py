from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Subject, Test

class HomeView(ListView):
    model = Subject
    template_name = 'core/home.html'
    context_object_name = 'subjects'

@login_required
def dashboard_view(request):
    recent_sessions = request.user.test_sessions.all().order_by('-start_time')[:5]
    
    available_tests = Test.objects.filter(is_published=True)
    
    subjects_with_tests = Subject.objects.all()
    
    context = {
        'recent_sessions': recent_sessions,
        'available_tests': available_tests,
        'subjects_with_tests': subjects_with_tests
    }
    
    return render(request, 'core/dashboard.html', context) 