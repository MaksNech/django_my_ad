from django.db import models
from decimal import Decimal
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_delete, post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
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
    INACTIVE = 100
    ACTIVE = 200
    DELETED = 300
    STATUS = (
        (INACTIVE, 'inactive'),
        (ACTIVE, 'active'),
        (DELETED, 'deleted'),
    )
    title = models.CharField(max_length=100)
    category = TreeForeignKey('Category', on_delete=models.CASCADE, related_name='ads')
    description = models.CharField(max_length=5000)
    img_count = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(8)],
                                                 blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0'), blank=True)
    negotiable_price = models.BooleanField(default=False, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    users = models.ManyToManyField(User, through='UserFavouriteAd', through_fields=('ad', 'user'),
                                   related_name='user_ad')
    status = models.IntegerField(
        choices=STATUS,
        default=ACTIVE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} | {} | {}".format(self.title, self.author, self.created_on)

    class Meta:
        ordering = ['-created_on']


class UserFavouriteAd(models.Model):
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='user_favourite_ad')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_favourite_ad')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Ad: {} | User: {}".format(self.ad, self.user)

    class Meta:
        ordering = ['-ad__created_on']


class Image(models.Model):
    img = models.FileField(upload_to='ads/')
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='images')
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        images = Image.objects.filter(ad=self.ad).count()
        if images > 7:
            raise ValidationError("Images")
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{} | {}".format(self.img, self.ad)

    class Meta:
        ordering = ['-created_on']


class ChatMessage(models.Model):
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    body = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Ad: {} | Author: {}".format(self.ad, self.author)

    class Meta:
        ordering = ['created_on']


# SIGNALS:  ############################################################################################################
# Begin

# delete img with Image model instance
@receiver(post_delete, sender=Image)
def image_img_delete(sender, instance, **kwargs):
    instance.img.delete(False)


# automatically generated Token to every rest api user
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# End
########################################################################################################################
