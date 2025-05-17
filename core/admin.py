from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Subject, Test, Question, Choice, UserAnswer, UserTestSession

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    fields = ('text', 'is_correct', 'order_index')

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'points', 'order')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by', 'is_published', 'created_at')
    list_filter = ('subject', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [QuestionInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'subject', 'created_by', 'is_published')
        }),
        (_('Даты'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'test', 'question_type', 'points', 'order')
    list_filter = ('test', 'question_type')
    search_fields = ('text', 'test__title')
    inlines = [ChoiceInline]
    
    def text_short(self, obj):
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text
    text_short.short_description = _('Текст вопроса')

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text_short', 'question', 'is_correct', 'order_index')
    list_filter = ('question__test', 'is_correct')
    search_fields = ('text', 'question__text')
    
    def text_short(self, obj):
        return f"{obj.text[:50]}..." if len(obj.text) > 50 else obj.text
    text_short.short_description = _('Текст варианта')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_short', 'test', 'is_correct', 'score_earned', 'timestamp')
    list_filter = ('user', 'test', 'is_correct', 'timestamp')
    search_fields = ('user__username', 'question__text', 'test__title')
    readonly_fields = ('timestamp',)
    
    def question_short(self, obj):
        return f"{obj.question.text[:30]}..." if len(obj.question.text) > 30 else obj.question.text
    question_short.short_description = _('Вопрос')

@admin.register(UserTestSession)
class UserTestSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'start_time', 'end_time', 'is_completed')
    list_filter = ('user', 'test', 'is_completed', 'start_time')
    search_fields = ('user__username', 'test__title')
    readonly_fields = ('start_time',) 