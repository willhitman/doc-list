# Generated by Django 5.0.1 on 2024-03-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_rename_date_create_insurance_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accessibility',
            name='insurance',
        ),
        migrations.AddField(
            model_name='accessibility',
            name='additional_notes',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='accessibility',
            name='pricing',
            field=models.CharField(blank=True, choices=[('Low', 'Low'), ('Mid', 'Mid'), ('High', 'High'), ('Expensive', 'Expensive')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='accessibility',
            name='wifi',
            field=models.BooleanField(default=False),
        ),
    ]
