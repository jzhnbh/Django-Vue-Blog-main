from rest_framework import serializers

from comment.models import Comment
from user_info.serializers import UserDescSerializer


class CommentChildrenSerializer(serializers.ModelSerializer):
    """
    子评论序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = ['parent', 'article']


class CommentSerializer(serializers.ModelSerializer):
    """
    评论序列化器
    """
    user = UserDescSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'created_at',
            'user',
            'article',
            'parent_id'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'article': {'required': True}
        }


