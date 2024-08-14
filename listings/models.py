from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
from utils.models import Address, Services, Languages

# from utils.languages.models import Languages

# Create your models here.
listing_types = (
    ("Doctor", "Doctor"),
    ("Locum", "Locum"),
    ("Practice", "Practice")
)


class Listing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    listing_type = models.CharField(max_length=50, choices=listing_types, null=True, blank=True)

    title = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    languages = models.ManyToManyField('ListingLanguages', blank=True)
    address = models.OneToOneField(Address, max_length=50, null=True, blank=True, on_delete=models.CASCADE)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'listing_type')

    def __str__(self):
        return f'{self.user.name}  {self.user.last_name}'


class ListingLanguages(models.Model):
    language = models.ForeignKey(Languages, max_length=50, null=True, blank=True, on_delete=models.CASCADE)
    proficiency = models.IntegerField(null=True, blank=True, validators=[MaxValueValidator(10)])

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.language}'


class ListingSpecialization(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    board_or_certification = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.board_or_certification


class ListingAffiliationsAndMemberships(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


class ListingEducationalBackground(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    school = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return {self.school}


Type = (
    ('Clinic', 'Clinic'),
    ('Hospital', 'Hospital')
)


class ListingExperience(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    years_of_experience = models.CharField(max_length=50, null=True, blank=True)
    practice = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.listing


class AppointmentsAvailability(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    days = models.ManyToManyField(to='Days')
    average_wait_time = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.days


class Days(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class ListingReviews(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)

    ratings = models.ManyToManyField(to='Rating')
    testimonial = models.CharField(max_length=50, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.listing


class Rating(models.Model):
    rate = models.IntegerField(default=0,
                               validators=[MinValueValidator(0), MaxValueValidator(5)],
                               help_text="Must be between 0 and 5 inclusive")

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)


class ListingServices(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    service = models.OneToOneField(Services, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(max_length=100, default=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.service.name
