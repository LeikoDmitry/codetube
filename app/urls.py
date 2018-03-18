from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import action

app_name = 'tube'
urlpatterns = [
    path('', action.Auth.index_action, name='index'),
    path('login', action.Auth.login_action, name='login'),
    path('register', action.Auth.register_action, name='register'),
    path('reset', action.Auth.reset_action, name='reset'),
    path('email', action.Auth.email_action, name='email'),
    path('logout', action.Auth.logout_action, name='logout'),
    path('channel/<channel>/setting', action.ChannelPages.setting_action, name='channel_setting'),
    path('channel/<channel>/edit', action.ChannelPages.edit_action, name='channel_edit'),
    path('upload', action.UploadVideo.index_action, name='upload_video'),
    path('video', action.UploadVideo.store, name='video'),
    path('video/<video>', action.UploadVideo.update, name='video_update'),
    path('video/store/upload', action.UploadVideo.store_file, name='video_upload_store')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)