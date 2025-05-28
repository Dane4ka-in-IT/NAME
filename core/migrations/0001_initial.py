from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Choice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст варианта")),
                (
                    "is_correct",
                    models.BooleanField(default=False, verbose_name="Правильный ответ"),
                ),
                (
                    "order_index",
                    models.PositiveIntegerField(
                        blank=True, default=0, null=True, verbose_name="Индекс порядка"
                    ),
                ),
            ],
            options={
                "verbose_name": "Вариант ответа",
                "verbose_name_plural": "Варианты ответов",
                "ordering": ["order_index"],
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст вопроса")),
                (
                    "question_type",
                    models.CharField(
                        choices=[
                            ("MC", "Множественный выбор"),
                            ("OA", "Открытый ответ"),
                            ("ORD", "Упорядочивание"),
                        ],
                        default="MC",
                        max_length=3,
                        verbose_name="Тип вопроса",
                    ),
                ),
                (
                    "points",
                    models.PositiveIntegerField(default=1, verbose_name="Баллы"),
                ),
                (
                    "order",
                    models.PositiveIntegerField(default=0, verbose_name="Порядок"),
                ),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Предмет",
                "verbose_name_plural": "Предметы",
            },
        ),
        migrations.CreateModel(
            name="Test",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "is_published",
                    models.BooleanField(default=False, verbose_name="Опубликован"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
            ],
            options={
                "verbose_name": "Тест",
                "verbose_name_plural": "Тесты",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="UserAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "submitted_text",
                    models.TextField(
                        blank=True, null=True, verbose_name="Текст ответа"
                    ),
                ),
                (
                    "ordered_choices_submission",
                    models.JSONField(
                        blank=True, null=True, verbose_name="Порядок вариантов"
                    ),
                ),
                (
                    "is_correct",
                    models.BooleanField(default=False, verbose_name="Правильный ответ"),
                ),
                (
                    "score_earned",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Заработанные баллы"
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время ответа"
                    ),
                ),
            ],
            options={
                "verbose_name": "Ответ пользователя",
                "verbose_name_plural": "Ответы пользователей",
                "ordering": ["-timestamp"],
            },
        ),
        migrations.CreateModel(
            name="UserTestSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_order", models.JSONField(verbose_name="Порядок вопросов")),
                (
                    "current_question_index",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Текущий индекс вопроса"
                    ),
                ),
                (
                    "start_time",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время начала"
                    ),
                ),
                (
                    "end_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время окончания"
                    ),
                ),
                (
                    "is_completed",
                    models.BooleanField(default=False, verbose_name="Завершен"),
                ),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to="core.test",
                        verbose_name="Тест",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сессия теста",
                "verbose_name_plural": "Сессии тестов",
                "ordering": ["-start_time"],
            },
        ),
    ] 