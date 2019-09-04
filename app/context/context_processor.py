from django.shortcuts import get_object_or_404
from app.models import Channel


def index_context(request):
    context_data = dict()
    if request.user.is_authenticated:
        try:
            context_data['user_channel'] = Channel.objects.get(users=request.user)
        except Channel.DoesNotExist:
            context_data['user_channel'] = {}
    return context_data
