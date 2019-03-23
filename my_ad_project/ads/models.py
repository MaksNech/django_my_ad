from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Ad(models.Model):
    title = models.CharField(max_length=100)
    category = TreeForeignKey('Category', on_delete=models.CASCADE, related_name='ads')
    description = models.CharField(max_length=5000)
    img_count = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(8)],
                                                 blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0'), blank=True)
    negotiable_price = models.BooleanField(default=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} | {} | {}".format(self.title, self.author, self.created_on)

    class Meta:
        ordering = ['-created_on']


class Image(models.Model):
    img = models.FileField(upload_to='ads/')
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='images')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} | {}".format(self.img, self.ad)

    class Meta:
        ordering = ['-created_on']
