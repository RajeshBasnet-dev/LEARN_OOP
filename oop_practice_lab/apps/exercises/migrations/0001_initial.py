# Generated for OOP Practice Lab MVP.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Exercise",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("difficulty", models.CharField(choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")], max_length=10)),
                ("starter_code", models.TextField()),
                ("expected_behavior", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["difficulty", "created_at"]},
        ),
        migrations.CreateModel(
            name="OOPConcept",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=50, unique=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="TestCase",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(max_length=200)),
                ("check_type", models.CharField(max_length=50)),
                ("check_target", models.CharField(max_length=100)),
                ("check_args", models.JSONField(default=dict)),
                ("exercise", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="exercises.exercise")),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.AddField(
            model_name="exercise",
            name="concepts",
            field=models.ManyToManyField(to="exercises.oopconcept"),
        ),
    ]
