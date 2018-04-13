from rest_framework import serializers
from app.models.entity import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'user', 'reply_id', 'body', 'create_at', 'video')
        depth = 2

