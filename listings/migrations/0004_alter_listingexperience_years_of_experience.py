# Generated by Django 5.0.6 on 2024-09-08 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_listing_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingexperience',
            name='years_of_experience',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
