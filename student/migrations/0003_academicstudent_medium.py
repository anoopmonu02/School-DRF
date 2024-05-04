# Generated by Django 5.0.3 on 2024-05-04 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_registerstudent_guardian_contact_and_more'),
        ('universal', '0002_alter_city_province'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicstudent',
            name='medium',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, related_name='academicstudentmediums', to='universal.medium'),
        ),
    ]