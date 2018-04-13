from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import action, view_classes

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
    path('video/<video>/delete', action.UploadVideo.delete_video, name='video_delete'),
    path('videos', action.UploadVideo.main_index, name='videos'),
    path('videos/<video>/views', view_classes.VideoView.as_view(), name='videos_views'),
    path('videos/<uid>/edit', action.UploadVideo.edit_video, name='video_edit'),
    path('videos/<uid>/votes', view_classes.VideoVoteShow.as_view(), name='video_votes_show'),
    path('videos/<uid>/votes/create', view_classes.VideoVoteCreate.as_view(), name='video_votes_create'),
    path('videos/<uid>/votes/remove', view_classes.VideoVoteRemove.as_view(), name='video_votes_remove'),
    path('video/store/upload', action.UploadVideo.store_file, name='video_upload_store'),
    path('webhook/encoding', view_classes.EncodingWebHook.as_view(), name='web_hook_encoding'),
    path('videos/<slug>/detail', view_classes.VideoShow.as_view(), name='video_detail'),
    path('search', view_classes.Search.as_view(), name='search'),
    path('videos/<uid>/comments', view_classes.CommentViewList.as_view(), name='videos_comments'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)