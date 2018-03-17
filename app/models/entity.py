from django.db import models
from django.contrib.auth.models import User


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
    image_filename = models.CharField(max_length=255, null=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

class UploadFile(models.Model):
    file = models.ImageField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)

    def get_file_name(self):
        return self.file.name
