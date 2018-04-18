from rest_framework import serializers
from app.models.entity import Comment


class CommentSerializer(serializers.ModelSerializer):

    image_channel = serializers.SerializerMethodField()

    def get_image_channel(self, obj):
        return obj.video.channel.get_file_name()

    class Meta:
        model = Comment
        fields = ('id', 'reply_id', 'body', 'create_at', 'video', 'image_channel')
        depth = 2
