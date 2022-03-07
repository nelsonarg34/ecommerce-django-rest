from django.db import models

from business.constants import (
        CATALOG_TYPE_CHOICE,
        CATALOG_CART,
)


def catalog_image(instance, filename):
    return 'images/catalog/{0}.jpg'.format(instance.slug)


class DayOfWeek(models.Model):

    DAY_OF_THE_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),        
    )
    name = models.CharField(max_length=20,choices=DAY_OF_THE_WEEK, unique=True)

    class Meta:
        verbose_name = 'Day'
        verbose_name_plural = 'Days'  

    def __str__(self):
        return self.name

class Catalog(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    type_of_catalog = models.CharField(max_length=30, choices=CATALOG_TYPE_CHOICE, default=CATALOG_CART)
    description = models.TextField()
    available_for_time = models.TimeField(default="00:00:00")
    available_to_time = models.TimeField(default="00:00:00")
    days_available = models.ManyToManyField(DayOfWeek)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to=catalog_image, null=True, blank=True)
    image1 = models.ImageField(upload_to=catalog_image, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'catalog'
        verbose_name_plural = 'catalogs'

    def __str__(self):
        return self.name