# Generated by Django 5.0.6 on 2024-08-16 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_rename_end_date_listingspecialization_date_issued_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listingspecialization',
            name='status',
            field=models.CharField(blank=True, default='active', max_length=20, null=True),
        ),
    ]
