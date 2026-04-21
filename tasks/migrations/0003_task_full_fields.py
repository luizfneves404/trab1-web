import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_task"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="description",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[("low", "Baixa"), ("medium", "Média"), ("high", "Alta")],
                default="medium",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pendente"),
                    ("in_progress", "Em andamento"),
                    ("done", "Concluída"),
                ],
                default="pending",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="task",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="planned_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
