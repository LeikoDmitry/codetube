from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from app.models import Video

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
                if method == 'video-created':
                    self.video_created(request)
                if method == 'video-encoded':
                    self.video_encoded(request)
                if method == 'encoding-progress':
                    self.video_progress(request)
            return redirect('tube:web_hook_encoding')
        except AttributeError:
            return redirect('tube:web_hook_encoding')

    def video_created(self, request):
        return False

    def video_encoded(self, request):
        file = self.get_video_by_filename(request.POST['original_filename'])
        file.processed = True
        file.video_id = request.POST['encoding_ids[0]']
        return file.save()

    def video_progress(self, request):
        file = self.get_video_by_filename(request.POST['original_filename'])
        file.processed_percent = request.POST['progress']
        return file.save()

    def get_video_by_filename(self, name):
        return Video.objects.get(video_filename=name)
