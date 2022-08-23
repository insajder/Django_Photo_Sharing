import uuid

from django.db import models
import datetime
import os
from .utils import get_filtered_image
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.


class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    birthday = models.DateField()
    description = models.CharField(max_length=250, blank=True, null=True)
    profile_photo_path = models.ImageField(null=True, blank=True, upload_to='images/')

    class Meta:
        managed = False
        db_table = 'user'

EFFECT_CHOICE = (
    ('NO_FILTER', 'no filter'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', 'blurred'),
    ('BINARY', 'binary'),
    ('INVERT', 'invert'),
)
def update_filename(instance, filename):
    return os.path.join(f'images/{instance.id_user}', filename)

class Photo(models.Model):
    id_photo = models.AutoField(primary_key=True)
    id_user = models.IntegerField()
    description = models.CharField(max_length=250, blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    setup = models.DateTimeField()
    photo_path = models.ImageField(upload_to=update_filename)
    effect = models.CharField(max_length=45, blank=True, null=True, choices=EFFECT_CHOICE)
    like = models.IntegerField()

    def save(self, *args, **kwargs):
        pil_img = Image.open(self.photo_path)
        cv_img = np.array(pil_img)
        img = get_filtered_image(cv_img, self.effect)

        im_pil = Image.fromarray(img)

        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()

        self.photo_path.save(str(self.photo_path), ContentFile(image_png), save=False)

        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'photo'

class Follower(models.Model):
    id_follower = models.AutoField(primary_key=True)
    id_user = models.IntegerField()
    id_user_follower = models.IntegerField()
    status = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'follower'

class Likes(models.Model):
    id_likes = models.AutoField(primary_key=True)
    id_user = models.IntegerField()
    id_photo = models.IntegerField()
    id_user_like = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'likes'

class Messages(models.Model):
    id_messages = models.AutoField(primary_key=True)
    id_user_receiver = models.CharField(max_length=45)
    id_user_sender = models.CharField(max_length=45)
    text = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'messages'

class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    sender = models.CharField(max_length=45, null=True, blank=True,)
    message = models.CharField(null=True, blank=True, max_length=45)
    thread_name = models.CharField(null=True, blank=True, max_length=45)
    timestamp = models.DateTimeField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'chat'