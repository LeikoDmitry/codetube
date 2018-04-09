from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from app.models import Video, Channel, VideoView as VideoViewModel
from algoliasearch_django import raw_search


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
            return render(request, self.template_name)
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
        context['uid'] = self.get_object().uid
        return context
    def __str__(self):
        return Video.title

class VideoView(TemplateView):
    """
    Add count views video
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Create count views video
        """
        if request.is_ajax():
            user = request.user
            try :
                video = Video.objects.get(uid=self.kwargs['video'])
                ip = request.META.get('REMOTE_ADDR')
                VideoViewModel.objects.create(user=user, video=video, ip=ip)
                message = video.uid
            except Video.DoesNotExist:
                message = 'Does not exist'
            return JsonResponse({
                'response': message
            })
        else:
            return redirect('tube:videos')

class Search(TemplateView):
    """
    Search at website
    """
    template_name = 'app/search.html'

    def get(self, request, *args, **kwargs):
        """
        Get method with params
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        query = request.GET['q']
        if query == '':
            return redirect('tube:index')
        ids_response = []
        ids_response_videos = []
        response = raw_search(Channel, query)
        response_video = raw_search(Video, query)
        for val in response['hits']:
            ids_response.append(val['objectID'])
        for val in response_video['hits']:
            ids_response_videos.append(val['objectID'])
        if (len(ids_response)) > 0:
            channels = Channel.objects.filter(id__in=ids_response)
        else:
            channels = ''
        if (len(ids_response_videos)) > 0:
            videos = Video.objects.filter(id__in=ids_response_videos)
        else:
            videos = ''
        return render(request, self.template_name, {
            'q': query,
            'channels': channels,
            'videos': videos
        })