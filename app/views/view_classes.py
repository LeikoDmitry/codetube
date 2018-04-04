from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from app.models import Video, UploadFile, Channel

class EncodingWebHook(TemplateView):

    template_name = 'app/hook_encoding.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                method = request.POST['event'].lower()
                if method == 'video-encoded':
                    self.video_encoded(request)
                elif method == 'encoding-progress':
                    self.video_progress(request)
            return redirect('tube:web_hook_encoding')
        except AttributeError:
            return redirect('tube:web_hook_encoding')

    def video_encoded(self, request):
        if 'original_filename' in request.POST:
            file = self.get_video_by_filename(request.POST['original_filename'])
            if file is not False:
                file.processed = True
                file.video_id = request.POST['encoding_ids[0]']
                return file.save()

    def video_progress(self, request):
        if 'original_filename' in request.POST:
            file = self.get_video_by_filename(request.POST['original_filename'])
            if file is not False:
                file.processed_percent = request.POST['progress']
                return file.save()

    def get_video_by_filename(self, name):
        try:
            return Video.objects.get(video_filename=name)
        except Video.DoesNotExist:
            return False


class VideoShow(DetailView):
    template_name = 'app/video_show.html'
    model = Video
    slug_field = 'uid'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        channel = Channel.objects.get(users=user)
        try:
            file = UploadFile.objects.get(channel=channel)
        except UploadFile.DoesNotExist:
            file = ''
        context['image_channel'] = file
        return context
    def __str__(self):
        return Video.title