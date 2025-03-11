from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify

# Create your models here.
class Profile(models.Model):
    USER_TYPE = [
        ("Customer", "Customer"),
        ("Admin", "Admin"),
        ("Barber", "Barber"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(upload_to="media", default="user-default.jpg",blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    user_type = models.CharField(max_length=50, choices=USER_TYPE)
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
    
class Specialty(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class BarberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,  blank=True)
    name = models.CharField(max_length=200, default="barber", null=True, blank=True)
    photo = models.ImageField(upload_to='media/barbers/', default="user-default.jpg", null=True, blank=True)
    experience = models.PositiveIntegerField(help_text="Years of experience",null=True,blank=True)
    availability = models.CharField(max_length=100, null=True, blank=True, default="")  # Example: "Mon-Fri, 9 AM - 6 PM"
    specialties = models.ManyToManyField(Specialty, related_name="barbers")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def average_rating(self):
        return Review.objects.filter(barber=self).aggregate(avg_rating=models.Avg('rating'))['avg_rating']
    
    def reviews(self):
        return Review.objects.filter(barber=self)
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug  = slugify(self.name)
        super(BarberProfile, self).save(*args, **kwargs)
        
class Review(models.Model):
    RATINGS = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    barber = models.ForeignKey(BarberProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviews')
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(choices=RATINGS, default=None)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} review on {self.product.name}'
    
    
class Services(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug  = slugify(self.name)
        super(Services, self).save(*args, **kwargs)
    
