from django.db import models
from django.contrib.auth.models import User
import os


class Token(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.value



class Channel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UploadFile(models.Model):
    file = models.ImageField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)

    def get_file_name(self):
        return self.file.name

    def get_file_extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    def __str__(self):
        return self.file

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    processed = models.BooleanField(default=False)
    video_id = models.CharField(max_length=255, null=True)
    video_filename = models.CharField(max_length=255, null=True)
    visibility = models.CharField(max_length=255, choices=(
        ('1', 'Public'),
        ('2', 'Unlisted'),
        ('3', 'Private'),
    ), default=1)
    allow_votes = models.BooleanField(default=False)
    allow_comment = models.BooleanField(default=True)
    processed_percent = models.IntegerField(null=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class UploadVideoFile(models.Model):
    video = models.FileField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def get_file_name(self):
        return self.video.name
