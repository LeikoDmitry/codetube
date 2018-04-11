import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from app.context.functions import get_file_path


class Token(models.Model):
    """
    Token generate for reset password
    """
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Return name for admin panel
        :return: string
        """
        return self.value



class Channel(models.Model):
    """
    Channel's user
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    file_name = models.FileField(upload_to=get_file_path, null=True, blank=True,)
    description = models.TextField(blank=True, null=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def get_file_name(self):
        """
        Return path image
        :return: string
        """
        return settings.BUCKETS_URL['IMAGE'] + '/profile/' + str(self.file_name.name)

    def get_file(self):
        """
        Return name image
        :return: string
        """
        return self.file_name.name

    def get_file_extension(self):
        """
        Return extension image
        :return: string
        """
        name, extension = os.path.splitext(self.file_name.name)
        return extension


    def __str__(self):
        """
        Return name for admin panel
        :return: string
        """
        return self.name

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

    def get_thumb(self):
        if self.processed is False:
            return settings.BUCKETS_URL['VIDEO'] + '/default.png'
        else:
            return settings.BUCKETS_URL['VIDEO'] + '/' + str(self.video_id) + '_1.jpg'

    def is_private(self):
        return bool(str(self.visibility) == '3')

    def get_stream_url(self):
        return settings.BUCKETS_URL['VIDEO'] + '/' + str(self.video_id) + '.mp4'

class UploadVideoFile(models.Model):
    video = models.FileField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def get_file_name(self):
        return self.video.name

class VideoView(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    ip = models.CharField(null=True, max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip

    @staticmethod
    def get_ip_user(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        elif request.META.get('HTTP_X_REAL_IP'):
            ip = request.META.get('HTTP_X_REAL_IP')
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LikeAble(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    like_able_id = models.IntegerField()
    like_able_type = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now=True)

class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=255, choices=(
        ('1', 'up'),
        ('2', 'down')
    ))
    created_at = models.DateTimeField(auto_now=True)