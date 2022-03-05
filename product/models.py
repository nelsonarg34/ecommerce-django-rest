from django.db import models
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from datetime import datetime


def product_image(instance, filename):
    return 'images/{0}.jpg'.format(instance.slug)


def user_images(instance, filename):
    date_time = datetime.now().strftime("%Y_%m_%d,%H:%M:%S")
    saved_file_name = instance.user.username + "-" + date_time + ".jpg"
    return 'profile/{0}/{1}'.format(instance.user.username, saved_file_name)



class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    is_lux = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset().filter(is_available=True, stock__gte=1)


class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)
    category = models.ForeignKey(Category, related_name="products_category", null=True, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    objects = models.Manager()
    available = AvailableManager()
    image = models.ImageField(upload_to=product_image, null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return "{}".format(self.id)