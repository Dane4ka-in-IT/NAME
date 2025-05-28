from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import Test, Question, Choice, Subject


class TestForm(forms.ModelForm):
    
    class Meta:
        model = Test
        fields = ['title', 'description', 'subject', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'points']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'})
        }


class ChoiceForm(forms.ModelForm):
    
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


def get_choice_formset(question=None):
    extra = 0 if question and question.pk else 2
    return inlineformset_factory(
        Question, 
        Choice,
        form=ChoiceForm,
        extra=extra,
        can_delete=True
    )


class SubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        } 