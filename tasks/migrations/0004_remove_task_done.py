from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_task_full_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="done",
        ),
    ]
