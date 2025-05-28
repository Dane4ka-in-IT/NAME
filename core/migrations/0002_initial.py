from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usertestsession",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="test_sessions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="useranswer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_answers",
                to="core.question",
                verbose_name="Вопрос",
            ),
        ),
        migrations.AddField(
            model_name="useranswer",
            name="selected_choices",
            field=models.ManyToManyField(
                blank=True,
                related_name="selected_by",
                to="core.choice",
                verbose_name="Выбранные варианты",
            ),
        ),
        migrations.AddField(
            model_name="useranswer",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_answers",
                to="core.test",
                verbose_name="Тест",
            ),
        ),
        migrations.AddField(
            model_name="useranswer",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AddField(
            model_name="test",
            name="created_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_tests",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Создатель",
            ),
        ),
        migrations.AddField(
            model_name="test",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tests",
                to="core.subject",
                verbose_name="Предмет",
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="core.test",
                verbose_name="Тест",
            ),
        ),
        migrations.AddField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="choices",
                to="core.question",
                verbose_name="Вопрос",
            ),
        ),
    ] 