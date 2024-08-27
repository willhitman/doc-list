# Generated by Django 5.0.6 on 2024-08-17 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_rename_end_date_listingaffiliationsandmemberships_date_issued_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listingeducationalbackground',
            old_name='degree',
            new_name='institute',
        ),
        migrations.RenameField(
            model_name='listingeducationalbackground',
            old_name='school',
            new_name='major',
        ),
        migrations.AddField(
            model_name='listingeducationalbackground',
            name='specialization',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='listingeducationalbackground',
            name='status',
            field=models.CharField(blank=True, default='pending', max_length=20, null=True),
        ),
    ]
