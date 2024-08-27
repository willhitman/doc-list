# Generated by Django 5.0.6 on 2024-08-21 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0015_alter_appointmentsavailability_average_wait_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingservices',
            name='availability',
            field=models.CharField(blank=True, choices=[('On Appointment', 'On Appointment'), ('Working Hours', 'Working Hours')], max_length=20, null=True),
        ),
    ]
