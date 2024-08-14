from django.db import models


# Create your models here.
class Address(models.Model):
    door_address = models.CharField(max_length=255, blank=True, null=True)
    street_one = models.CharField(max_length=255, blank=True, null=True)
    street_two = models.CharField(max_length=255, blank=True, null=True)
    suburb = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.door_address


class Insurance(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Languages(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Accessibility(models.Model):
    pricing_choices = (
        ('Low', 'Low'),
        ('Mid', 'Mid'),
        ('High', 'High'),
        ('Expensive', 'Expensive')
    )
    insurance_choices = (
        ('Yes', 'Yes'),
        ('Cash Only', 'Cash Only')
    )
    languages = models.ManyToManyField(Languages)
    parking = models.BooleanField(default=False)
    wheel_chair_accessible_parking = models.BooleanField(default=True)
    wifi = models.BooleanField(default=False)
    infotainment = models.BooleanField(default=False)
    pricing = models.CharField(max_length=10, choices=pricing_choices, null=True, blank=True)
    additional_notes = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.infotainment


class Services(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


