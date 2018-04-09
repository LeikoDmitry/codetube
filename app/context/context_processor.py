from app.models import Channel

def index_context(request):
    context_data = dict()
    if request.user.is_authenticated:
       context_data['channel'] = Channel.objects.get(users=request.user)
    return context_data
