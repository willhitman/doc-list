import os
import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
from utils.models import Address, Services, Languages
from django.core.exceptions import ValidationError
from django.utils import timezone
from dateutil.relativedelta import relativedelta

# Create your models here.
listing_types = (
    ("Doctor", "Doctor"),
    ("Locum", "Locum"),
    ("Practice", "Practice"),
    ("Nurse", "Nurse")
)


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    listing_type = models.CharField(max_length=50, choices=listing_types, null=True, blank=True)

    title = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles', blank=True, null=True)
    languages = models.ManyToManyField('ListingLanguages', blank=True)
    address = models.OneToOneField(Address, max_length=50, null=True, blank=True, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'listing_type')

    def __str__(self):
        return f'{self.user.first_name}  {self.user.last_name}'


class ListingLanguages(models.Model):
    language = models.ForeignKey(Languages, null=True, blank=True, on_delete=models.CASCADE)
    proficiency = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.language}'


class ListingSpecialization(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    board_or_certification = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)

    date_issued = models.DateField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.board_or_certification

    # method for validation before saving
    def clean(self):
        super().clean()
        if self.date_issued is None:
            raise ValidationError("Date Issued cannot be null")
        elif self.date_issued > timezone.now().date():
            raise ValidationError("Date Issued cannot be in the future")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ListingAffiliationsAndMemberships(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)

    date_issued = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, default="active", null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    # method for validation before saving
    def clean(self):
        super().clean()

        if self.date_issued >= self.expiry_date:
            raise ValidationError("Date issued cannot be before or equal to Expiry date")

        if self.date_issued and self.date_issued > timezone.now().date():
            raise ValidationError("Date Issued cannot be in the future")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ListingEducationalBackground(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    institute = models.CharField(max_length=50, null=True, blank=True)
    major = models.CharField(max_length=50, null=True, blank=True)
    specialization = models.CharField(max_length=50, null=True, blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, default="pending", null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return {self.institute}

    # method for validation before saving
    def clean(self):
        super().clean()

        if self.start_date and self.start_date > timezone.now().date():
            raise ValidationError("Start date cannot be in the future")

        if self.end_date and self.end_date < timezone.now().date():
            self.status = 'finished'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ListingExperience(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    years_of_experience = models.CharField(null=True, blank=True,
                                           max_length=30)  #field is calculated don't bother provide it
    # will be overwritten

    skill = models.CharField(max_length=50, null=True, blank=True)

    practice = models.CharField(max_length=50, null=True, blank=True)

    duties = models.CharField(max_length=200, null=True, blank=True)

    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)

    still_employed = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.listing

    # method for validation before saving
    def clean(self):
        super().clean()

        if (self.date_from and self.date_to) and (self.date_from >= self.date_to):
            raise ValidationError("Date From cannot be after or equal to Date to")

        if self.date_from and self.date_from > timezone.now().date():
            raise ValidationError("Date From cannot be in the future")

        if self.date_to and self.date_to < timezone.now().date():
            self.still_employed = False

    def save(self, *args, **kwargs):
        self.clean()
        if self.date_to < timezone.now().date():
            date = relativedelta(self.date_to, self.date_from)
        else:
            date = relativedelta(timezone.now().date(), self.date_from)
        self.years_of_experience = f'{date.years} years, {date.months} months'
        super().save(*args, **kwargs)


class AppointmentsAvailability(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)

    days = models.ManyToManyField(to='utils.Days')

    average_wait_time = models.IntegerField(help_text="Expressed in hours as an Integer", null=True, blank=True,
                                            validators=[MinValueValidator(1), MaxValueValidator(20)])

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    # method to make sure no residue data will remain in the table create to support the many-to-many field
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # After saving the instance, remove related days if they are empty or not assigned
        if not self.days.exists():
            self.days.clear()

    def __str__(self):
        return self.days


class ListingReviews(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)

    ratings = models.ManyToManyField(to='Rating')
    testimonial = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    # method to make sure no residue data will remain in the table create to support the many-to-many field
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # After saving the instance, remove related days if they are empty or not assigned
        if not self.ratings.exists():
            self.ratings.clear()

    def __str__(self):
        return self.listing


class Rating(models.Model):
    rate = models.IntegerField(default=0,
                               validators=[MinValueValidator(0), MaxValueValidator(5)],
                               help_text="Must be between 0 and 5 inclusive")

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)


availability = (
    ("On Appointment", "On Appointment"),
    ("Working Hours", "Working Hours")
)


class ListingServices(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)

    service = models.ForeignKey(Services, on_delete=models.CASCADE, null=True, blank=True)

    description = models.CharField(max_length=500, null=True, blank=True)

    is_active = models.BooleanField(max_length=6, default=True)

    availability = models.CharField(choices=availability, max_length=20, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('listing', 'service')

    def __str__(self):
        return self.service.name
