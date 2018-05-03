from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from app.forms.form import UserRegistrationForm, ResetForm, UpdateChannelForm, VideoForm
from app.models import Token, Channel, Video, UploadVideoFile
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import os
import boto3



class Auth:
    """Auth classes action"""

    @staticmethod
    @login_required(login_url='/login')
    def index_action(request):
        limit = 5
        user_video = Channel.objects.get(users=request.user).video_set.all().filter(processed=True).order_by('-created_at')[:limit]
        return render(request, 'app/index.html', {
            'subscribtion_videos': user_video,
        })

    @staticmethod
    def login_action(request):
        if request.method != 'POST':
            return render(request, 'app/login.html')
        else:
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = User.objects.get(email=email)
                user_login = authenticate(request, username=user.username, password=password)
                if user_login is not None:
                    login(request, user_login)
                    return redirect('tube:index')
                else:
                    messages.error(request, message='Wrong password or email')
                    return redirect('tube:login')
            except User.DoesNotExist:
                messages.error(request, message='Wrong password or email')
                return redirect('tube:login')

    @staticmethod
    def register_action(request):
        if request.method != 'POST':
            if 'form' in request.session:
                form = request.session['form']
                del request.session['form']
            else:
                form = ""
            return render(request, 'app/register.html', {
                'form': form
            })
        else:
            form = UserRegistrationForm(request.POST)
            if not form.is_valid():
                request.session['form'] = form.errors
                return redirect('tube:register')
            else:
                user_created = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                )
                if user_created:
                    Channel.objects.create(
                        name=form.cleaned_data['channel_name'],
                        slug=uuid.uuid4().hex[:8],
                        users=user_created
                    )
                    user_login = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                    login(request, user_login)
                    return redirect('tube:index')

    @staticmethod
    def reset_action(request):
        if request.method == 'POST':
            try:
                password = request.POST['password']
                user = User.objects.filter(email=request.POST['email'], token__value=request.POST['token']).first()
                user.set_password(raw_password=password)
                user.save()
                token_code = Token.objects.get(value=request.POST['token'])
                token_code.delete()
                return redirect('tube:index')
            except User.DoesNotExist:
                return redirect('tube:reset')
        if 'code' in request.GET:
            try:
                token = Token.objects.get(value=request.GET['code'])
                return render(request, 'app/reset.html', {'token': token})
            except Token.DoesNotExist:
                return redirect('tube:index')
        else:
            return redirect('tube:index')

    @staticmethod
    def email_action(request):
        if request.method != 'POST':
            if 'error' in request.session:
                error = request.session['error']
                del request.session['error']
            else:
                error = ""
            return render(request, 'app/email.html', {
                'error': error
            })
        else:
            try:
                email = request.POST['email']
                form = ResetForm(request.POST)
                if not form.is_valid():
                    request.session['error'] = form.errors
                    return redirect('tube:email')
                else:
                    user_reset = User.objects.get(email=email)
                    code = get_random_string(length=32)
                    Token.objects.create(value=code, user=user_reset)
                    subject, from_email, to = 'Reset password', 'admin@codetube', user_reset.email
                    html_content = render_to_string('app/reset_mail.html', {
                        'email': user_reset.email,
                        'url': 'http://' + request.get_host() + '/reset?code=' + code,
                    })
                    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    messages.info(request, 'All information send you in email.')
                    return redirect('tube:login')
            except User.DoesNotExist:
                return render(request, 'app/email.html')

    @staticmethod
    def logout_action(request):
        logout(request)
        return redirect('tube:login')


class ChannelPages:

    @staticmethod
    @login_required(login_url='/login')
    def setting_action(request, channel):
        my_channel = Channel.objects.get(users=request.user, slug=channel)
        if 'error' in request.session:
            error = request.session['error']
            del request.session['error']
        else:
            error = ""
        return render(request, 'app/channel_edit.html', {
            'my_channel': my_channel,
            'host': request.get_host(),
            'error': error
        })

    @staticmethod
    @login_required(login_url='/login')
    def edit_action(request, channel):
        if request.method == 'POST':
            my_channel = Channel.objects.get(users=request.user, slug=channel)
            form = UpdateChannelForm(request.POST, request.FILES, instance=my_channel)
            if form.is_valid():
                form.save()
                if 'file_name' in request.FILES:
                    file = form.instance.file_name.name
                    path = os.path.join(settings.MEDIA_ROOT, file)
                    size = 90, 90
                    im = Image.open(path)
                    im.thumbnail(size)
                    im.save(path, "PNG")
                    s3 = boto3.resource('s3')
                    data = open(path, 'rb')
                    s3.Bucket(settings.S3_BUCKET).put_object(Key='profile/' + file, Body=data)
                    os.remove(os.path.join(settings.MEDIA_ROOT, file))
                return redirect('tube:channel_setting', channel=my_channel.slug)
            else:
                request.session['error'] = form.errors
                return redirect('tube:channel_setting', channel=my_channel.slug)
        else:
            return redirect('tube:index')


class UploadVideo:

    @staticmethod
    @login_required(login_url='/login')
    def index_action(request):
        return render(request, 'app/video_upload.html')

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/login')
    def store(request):
        if request.method != 'POST':
            return JsonResponse({
                'response': 'get'
            })
        channel = Channel.objects.get(users=request.user)
        uid = uuid.uuid4().hex[:10]
        file_name = str(uid) + '.' + request.POST['extension']
        Video.objects.create(
            channel=channel,
            uid=uid,
            title=request.POST['title'],
            description=request.POST['description'],
            visibility=request.POST['visibility'],
            video_filename=file_name
        )
        response = JsonResponse({'uid': uid, 'file_name': file_name})
        return response

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/login')
    def update(request, video):
        video_user = Video.objects.get(uid=video)
        if video_user.channel.users_id == request.user.id:
            form = VideoForm(request.POST, instance=video_user)
            if form.is_valid():
                form.save()
                if request.is_ajax():
                    return JsonResponse({
                        'uid': video
                    })
                else:
                    return redirect('tube:video_edit', uid=video)
            else:
                return redirect('tube:video_edit', uid=video)

        else:
            return JsonResponse({
                'uid': '0'
            })

    @staticmethod
    @csrf_exempt
    @login_required(login_url='/login')
    def store_file(request):
        my_channel = Channel.objects.get(users=request.user)
        upload_video = UploadVideoFile(video=request.FILES['video'], channel=my_channel)
        upload_video.save()
        file_video_name = os.path.join(settings.MEDIA_ROOT, upload_video.get_file_name())
        file = upload_video.get_file_name()
        data = open(file_video_name, 'rb')
        s3 = boto3.resource('s3')
        if 'file_uid' in request.POST:
            uid_file = request.POST['file_uid']
            s3.Bucket(settings.S3_BUCKET_DROP).put_object(Key=uid_file, Body=data)
        os.remove(os.path.join(settings.MEDIA_ROOT, file))
        return JsonResponse({
            'uid': request.user.id
        })

    @staticmethod
    @login_required(login_url='/login')
    def main_index(request):
        try :
            user = request.user
            channel = Channel.objects.get(users=user)
            videos_user = Video.objects.filter(channel=channel).order_by('created_at')
        except Video.DoesNotExist:
            videos_user = ''
        return render(request, 'app/main_index.html', {
            'videos': videos_user
        })

    @staticmethod
    @login_required(login_url='/login')
    def edit_video(request, uid):
        try:
            video = Video.objects.get(uid=uid)
        except Video.DoesNotExist:
            video = ''
        return render(request, template_name='app/edit_video.html', context={
            'video': video
        })

    @staticmethod
    @login_required(login_url='/login')
    def delete_video(request, video):
        if request.method == 'POST':
            video_user = Video.objects.get(uid=video)
            if video_user.channel.users_id == request.user.id:
                video_user.delete()
                return redirect('tube:videos')
        else:
            return redirect('tube:videos')





