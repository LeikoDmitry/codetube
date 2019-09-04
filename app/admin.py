from django.contrib import admin
from .models import Video, Channel, Token, Vote, Subscriptions

admin.site.register(Video)
admin.site.register(Channel)
admin.site.register(Token)
admin.site.register(Vote)
admin.site.register(Subscriptions)
