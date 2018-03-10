from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.value


