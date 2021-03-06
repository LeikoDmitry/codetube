from django.views.generic import TemplateView, DetailView
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.exceptions import MultipleObjectsReturned
from app.models import Video, Channel, VideoView as VideoViewModel, Vote, Comment, Subscriptions
from app.serializers.serializes_classes import CommentSerializer
from algoliasearch_django import raw_search
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


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
            try:
                video = Video.objects.get(uid=self.kwargs['video'])
                ip = VideoViewModel.get_ip_user(request)
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
            ids_response.append(val.get('objectID'))
        for val in response_video['hits']:
            ids_response_videos.append(val.get('objectID'))
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


class VideoVoteShow(TemplateView):

    response = {
        'up': None,
        'down': None,
        'can_vote': False,
        'user_vote': None,
    }

    def get(self, request, *args, **kwargs):
        try:
            video = Video.objects.get(uid=self.kwargs['uid'])
            self.response['down'] = video.vote_set.filter(type='down').count()
            self.response['up'] = video.vote_set.filter(type='up').count()
            if video.allow_votes is True:
                self.response['can_vote'] = True
            else:
                self.response['can_vote'] = False
            if request.user.is_active:
                try:
                    vote_from_user = video.vote_set.get(user=request.user)
                    self.response['user_vote'] = vote_from_user.type
                except Vote.DoesNotExist:
                    self.response['user_vote'] = None
        except Video.DoesNotExist:
            self.response = {
                'data': None
            }
        return JsonResponse({
            'data': self.response
        })


class VideoVoteCreate(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            if user.is_active:
                try:
                    video = Video.objects.get(uid=kwargs['uid'])
                    if video.allow_votes is True:
                        try:
                            vote = Vote.objects.get(user=user, video=video)
                            vote.delete()
                        except Vote.DoesNotExist:
                            pass
                        Vote.objects.create(
                            type=request.POST['type'],
                            user=user,
                            video=video
                        )
                        message = True
                    else:
                        message = 'Can`t add vote'
                except Video.DoesNotExist:
                    message = 'Video not exist'
            else:
                message = 'You can not add your vote, need login or registration'

            return JsonResponse({
                'response': message
            })
        else:
            return redirect('tube:index')


class VideoVoteRemove(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            user = request.user
            if user.is_active:
                video = Video.objects.get(uid=kwargs['uid'])
                if video.allow_votes is True:
                    try:
                        vote = Vote.objects.get(user=user, video=video)
                        vote.delete()
                        result = True
                    except Vote.DoesNotExist:
                        result = False
                else:
                    result = 'Vote is can`t remove'
            else:
                result = 'You can not add your vote, need login or registration'
            return JsonResponse({
                'response': result
            })
        else:
            return redirect('tube:index')


class CommentViewList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    renderer_classes = (JSONRenderer, )

    def get_queryset(self):
        uid = self.kwargs['uid']
        try:
            video = Video.objects.get(uid=uid)
            try:
                comments = Comment.objects.filter(video=video)
            except Comment.DoesNotExist:
                comments = ''
            return comments
        except Video.DoesNotExist:
            return ''


class CommentViewCreate(generics.CreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        uid = kwargs['uid']
        video = Video.objects.get(uid=uid)
        user = self.request.user
        serializer = CommentSerializer(data=request.POST)
        if serializer.is_valid():
            if request.POST['reply_id'] == 'null':
                serializer.save(user=user, video=video)
            else:
                serializer.save(user=user, video=video, reply_id=Comment.objects.get(id=request.POST['reply_id']))
            queryset = self.get_queryset()
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChannelSubscribed(TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        channel = ''
        try:
            channel = Channel.objects.get(slug=kwargs['channel'])
            count = channel.subscriptions_set.count()
            response = {
                'count': count,
                'user_subscribed': False,
                'can_subscribe': False
            }
        except Channel.DoesNotExist:
            response = {
                'count': False,
                'user_subscribed': False,
                'can_subscribe': False
            }

        if request.user.is_active:
            try:
                Subscriptions.objects.get(channel=channel, user=request.user)
                response.update({
                    'user_subscribed': True,
                    'can_subscribe': False,
                })
            except Subscriptions.DoesNotExist:
                response.update({
                    'user_subscribed': False,
                    'can_subscribe': True,
                })
            except MultipleObjectsReturned:
                response.update({
                    'user_subscribed': False,
                    'can_subscribe': False,
                    'error': 'Can"t be else add user'
                })
            except ValueError:
                response.update({
                    'user_subscribed': False,
                    'can_subscribe': False,
                    'error': 'No channel"s name'
                })
        return JsonResponse(response)

    def put(self, request, *args, **kwargs):

        try:
            channel = Channel.objects.get(slug=kwargs['channel'])
            if request.user.is_active:
                Subscriptions.objects.create(user=request.user, channel=channel)
                return JsonResponse({
                    'response': True,
                    'count': channel.subscriptions_set.count()
                })
            else:
                return JsonResponse({
                    'response': 'Can"t subscribed, you must login or register',
                    'count': False
                })
        except Channel.DoesNotExist:
            return JsonResponse({
                'response': False,
                'count': False
            })

    def delete(self, request, *args, **kwargs):
        try:
            if request.user.is_active:
                channel = Channel.objects.get(slug=kwargs['channel'])
                subscribe_user = Subscriptions.objects.get(user=request.user, channel=channel)
                subscribe_user.delete()
                return JsonResponse({
                    'response': True,
                    'count': channel.subscriptions_set.count()
                })
            else:
                return JsonResponse({
                    'response': False,
                    'count': False
                })
        except Channel.DoesNotExist:
            return JsonResponse({
                'response': False,
                'count': False
            })
        except Subscriptions.DoesNotExist:
            return JsonResponse({
                'response': False,
                'count': False
            })


class ChannelPage(TemplateView):

    template_name = 'app/channel_page.html'

    def get(self, request, *args, **kwargs):
        try:
            channel = Channel.objects.get(slug=self.kwargs['channel'])
            try:
                videos = Video.objects.filter(channel=channel)[:5]
            except Video.DoesNotExist:
                videos = None
            return render(request, self.template_name, {
                'channel': channel,
                'videos': videos,
            })
        except Channel.DoesNotExist:
            return redirect('tube:index')
