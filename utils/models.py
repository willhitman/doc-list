from django.db import models

import listings.models


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

    insurance_choices = (
        ('Yes', 'Yes'),
        ('Cash Only', 'Cash Only')
    )
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, blank=True, null=True)
    parking = models.BooleanField(default=False)
    wheel_chair_accessible_parking = models.BooleanField(default=True)
    wifi = models.BooleanField(default=False)
    infotainment = models.BooleanField(default=False)
    additional_notes = models.CharField(max_length=300, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.infotainment


class Services(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


days = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday")
)


class Days(models.Model):
    day = models.CharField(choices=days, max_length=50, null=True, blank=True, unique=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.day}'
