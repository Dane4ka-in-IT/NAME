from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Subject, Test

class HomeView(ListView):
    model = Subject
    template_name = 'core/home.html'
    context_object_name = 'subjects'

class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'core/subject_detail.html'
    context_object_name = 'subject'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = Test.objects.filter(
            subject=self.object,
            is_published=True
        )
        return context

class TestListView(ListView):
    model = Test
    template_name = 'core/test_list.html'
    context_object_name = 'tests'
    
    def get_queryset(self):
        return Test.objects.filter(is_published=True)

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