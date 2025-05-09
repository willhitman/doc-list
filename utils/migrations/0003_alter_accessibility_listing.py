# Generated by Django 5.0.6 on 2024-09-26 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_alter_listing_profile_picture'),
        ('utils', '0002_alter_accessibility_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessibility',
            name='listing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='listings.listing', unique=True),
        ),
    ]
