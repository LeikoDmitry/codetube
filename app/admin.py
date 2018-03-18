from django.contrib import admin
from .models import Video, UploadFile, Channel, Token

admin.site.register(Video)
admin.site.register(UploadFile)
admin.site.register(Channel)
admin.site.register(Token)
