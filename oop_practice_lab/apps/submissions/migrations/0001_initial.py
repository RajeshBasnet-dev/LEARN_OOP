# Generated for OOP Practice Lab MVP.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exercises", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.TextField()),
                ("status", models.CharField(choices=[("pending", "Pending"), ("evaluated", "Evaluated"), ("error", "Error")], default="pending", max_length=20)),
                ("score", models.FloatField(null=True)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                ("exercise", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="exercises.exercise")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-submitted_at"]},
        ),
        migrations.CreateModel(
            name="FeedbackItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("level", models.CharField(choices=[("pass", "Pass"), ("fail", "Fail"), ("warning", "Warning"), ("info", "Info")], max_length=10)),
                ("check_name", models.CharField(max_length=100)),
                ("message", models.TextField()),
                ("submission", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="feedback", to="submissions.submission")),
            ],
        ),
    ]
