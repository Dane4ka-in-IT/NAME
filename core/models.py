from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(_('Название'), max_length=100)
    
    class Meta:
        verbose_name = _('Предмет')
        verbose_name_plural = _('Предметы')
    
    def __str__(self):
        return self.name

class Test(models.Model):
    title = models.CharField(_('Название'), max_length=200)
    description = models.TextField(_('Описание'))
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='tests',
        verbose_name=_('Предмет')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tests',
        verbose_name=_('Создатель')
    )
    is_published = models.BooleanField(_('Опубликован'), default=False)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = (
        ('MC', _('Множественный выбор')),
        ('OA', _('Открытый ответ')),
        ('ORD', _('Упорядочивание')),
    )
    
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_('Тест')
    )
    text = models.TextField(_('Текст вопроса'))
    question_type = models.CharField(
        _('Тип вопроса'),
        max_length=3,
        choices=QUESTION_TYPES,
        default='MC'
    )
    points = models.PositiveIntegerField(_('Баллы'), default=1)
    order = models.PositiveIntegerField(_('Порядок'), default=0)
    
    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
        ordering = ['order']
    
    def __str__(self):
        return f"{self.text[:50]}..." if len(self.text) > 50 else self.text

class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name=_('Вопрос')
    )
    text = models.TextField(_('Текст варианта'))
    is_correct = models.BooleanField(_('Правильный ответ'), default=False)
    order_index = models.PositiveIntegerField(_('Индекс порядка'), default=0, null=True, blank=True)
    
    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответов')
        ordering = ['order_index']
    
    def __str__(self):
        return f"{self.text[:50]}..." if len(self.text) > 50 else self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_('Пользователь')
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='user_answers',
        verbose_name=_('Вопрос')
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='user_answers',
        verbose_name=_('Тест')
    )
    submitted_text = models.TextField(_('Текст ответа'), blank=True, null=True)
    selected_choices = models.ManyToManyField(
        Choice,
        blank=True,
        related_name='selected_by',
        verbose_name=_('Выбранные варианты')
    )
    ordered_choices_submission = models.JSONField(_('Порядок вариантов'), blank=True, null=True)
    is_correct = models.BooleanField(_('Правильный ответ'), default=False)
    score_earned = models.PositiveIntegerField(_('Заработанные баллы'), default=0)
    timestamp = models.DateTimeField(_('Время ответа'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Ответ пользователя')
        verbose_name_plural = _('Ответы пользователей')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}..."

class UserTestSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_sessions',
        verbose_name=_('Пользователь')
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_('Тест')
    )
    question_order = models.JSONField(_('Порядок вопросов'))
    current_question_index = models.PositiveIntegerField(_('Текущий индекс вопроса'), default=0)
    start_time = models.DateTimeField(_('Время начала'), auto_now_add=True)
    end_time = models.DateTimeField(_('Время окончания'), null=True, blank=True)
    is_completed = models.BooleanField(_('Завершен'), default=False)
    
    class Meta:
        verbose_name = _('Сессия теста')
        verbose_name_plural = _('Сессии тестов')
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.test.title}" 