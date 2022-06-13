from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.


class Tier(models.Model):
    name = models.CharField(max_length=20)
    can_bigger_size = models.BooleanField(default=False)
    can_original_image = models.BooleanField(default=False)
    can_expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class CustomUser(AbstractUser):
    tier = models.ForeignKey(to='Tier', null=True, default=None, on_delete=models.CASCADE)


def nameFile(instance, filename):
    return f'images/{instance.user}-{filename}'


class ImageFile(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    original_image = models.ImageField(_("Original image"), upload_to=nameFile, blank=True, null=True)
    small_thumbnail = models.ImageField(_("Small thumbnail"), upload_to=nameFile, blank=True, null=True, editable=True)
    big_thumbnail = models.ImageField(_("Big thumbnail"), upload_to=nameFile, blank=True, null=True, editable=True)

    def __str__(self):
        return f'{self.user} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Wrong filetype.')

        small = self.make_thumbnail(new_height=200)
        self.small_thumbnail.save(small[0], small[1], save=False)

        big = self.make_thumbnail(new_height=400)
        self.big_thumbnail.save(big[0], big[1], save=False)

        super(ImageFile, self).save(*args, **kwargs)

    def make_thumbnail(self, new_height=200):
        image = Image.open(self.original_image)
        width, height = image.size
        new_width = new_height * width / height
        new_width = int(new_width)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.original_image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb_' + f'{new_height}' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False

        # Save thumbnail to file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        content = ContentFile(temp_thumb.read())
        temp_thumb.close()

        return thumb_filename, content


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_delete, sender=ImageFile)
def post_delete_image(sender, instance, *args, **kwargs):
    try:
        instance.original_image.delete(save=False)
        instance.small_thumbnail.delete(save=False)
        instance.big_thumbnail.delete(save=False)
    except:
        pass
