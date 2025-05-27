from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
import random

from .models import Subject, Test, Question, Choice, UserTestSession, UserAnswer

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

@login_required
def start_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id, is_published=True)
    
    existing_session = UserTestSession.objects.filter(
        user=request.user,
        test=test,
        is_completed=False
    ).first()
    
    if existing_session:
        session = existing_session
    else:
        questions = list(Question.objects.filter(test=test))
        
        random.shuffle(questions)
        
        question_order = [q.id for q in questions]
        session = UserTestSession.objects.create(
            user=request.user,
            test=test,
            question_order=question_order,
            current_question_index=0
        )
    
    return redirect('question_view', session_id=session.id)

@login_required
def question_view(request, session_id):
    session = get_object_or_404(
        UserTestSession,
        pk=session_id,
        user=request.user,
        is_completed=False
    )
    test = session.test
    
    if session.current_question_index >= len(session.question_order):
        return redirect('end_test', session_id=session.id)
    
    question_id = session.question_order[session.current_question_index]
    question = get_object_or_404(Question, pk=question_id)
    
    choices = []
    if question.question_type in ['MC', 'ORD']:
        choices = list(Choice.objects.filter(question=question))
        random.shuffle(choices)
    
    if request.method == 'POST':
        is_correct = False
        score_earned = 0
        
        if question.question_type == 'MC':
            selected_choice_ids = request.POST.getlist('choice')
            
            if not selected_choice_ids:
                return render(request, 'core/question.html', {
                    'session': session,
                    'test': test,
                    'question': question,
                    'choices': choices,
                    'current_index': session.current_question_index + 1,
                    'total_questions': len(session.question_order),
                    'error_message': 'Пожалуйста, выберите хотя бы один вариант ответа.'
                })
                
            selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
            
            correct_choices = Choice.objects.filter(question=question, is_correct=True)
            
            selected_correct = set(selected_choices.filter(is_correct=True))
            if (set(correct_choices) == selected_correct and 
                    len(selected_choices) == len(selected_correct)):
                is_correct = True
                score_earned = question.points
            
            user_answer = UserAnswer.objects.create(
                user=request.user,
                question=question,
                test=test,
                is_correct=is_correct,
                score_earned=score_earned
            )
            user_answer.selected_choices.set(selected_choices)
            
        elif question.question_type == 'OA':
            submitted_text = request.POST.get('answer', '').strip()
            
            if not submitted_text:
                return render(request, 'core/question.html', {
                    'session': session,
                    'test': test,
                    'question': question,
                    'choices': choices,
                    'current_index': session.current_question_index + 1,
                    'total_questions': len(session.question_order),
                    'error_message': 'Пожалуйста, введите ваш ответ.'
                })
            
            is_correct = True
            score_earned = question.points
            
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                test=test,
                submitted_text=submitted_text,
                is_correct=is_correct,
                score_earned=score_earned
            )
            
        elif question.question_type == 'ORD':
            ordered_choice_ids = request.POST.getlist('ordered_choice')
            
            if len(ordered_choice_ids) != Choice.objects.filter(question=question).count():
                return render(request, 'core/question.html', {
                    'session': session,
                    'test': test,
                    'question': question,
                    'choices': choices,
                    'current_index': session.current_question_index + 1,
                    'total_questions': len(session.question_order),
                    'error_message': 'Ошибка при сохранении порядка. Пожалуйста, попробуйте еще раз.'
                })
                
            ordered_choices = [int(choice_id) for choice_id in ordered_choice_ids]
            
            correct_order = list(Choice.objects.filter(question=question)
                               .order_by('order_index')
                               .values_list('id', flat=True))
            
            is_correct = ordered_choices == correct_order
            if is_correct:
                score_earned = question.points
            
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                test=test,
                ordered_choices_submission=ordered_choices,
                is_correct=is_correct,
                score_earned=score_earned
            )
        
        session.current_question_index += 1
        session.save()
        
        return redirect('question_view', session_id=session.id)
    
    return render(request, 'core/question.html', {
        'session': session,
        'test': test,
        'question': question,
        'choices': choices,
        'current_index': session.current_question_index + 1,
        'total_questions': len(session.question_order)
    })

@login_required
def end_test(request, session_id):
    session = get_object_or_404(
        UserTestSession,
        pk=session_id,
        user=request.user
    )
    
    if not session.is_completed:
        session.is_completed = True
        session.end_time = timezone.now()
        session.save()
    
    answers = UserAnswer.objects.filter(
        user=request.user,
        test=session.test,
        timestamp__gte=session.start_time,
        timestamp__lte=session.end_time or timezone.now()
    )
    
    total_score = sum(answer.score_earned for answer in answers)
    total_possible = sum(Question.objects.get(id=q_id).points 
                       for q_id in session.question_order)
    
    percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
    
    return render(request, 'core/results.html', {
        'session': session,
        'test': session.test,
        'answers': answers,
        'total_score': total_score,
        'total_possible': total_possible,
        'percentage': percentage
    }) 