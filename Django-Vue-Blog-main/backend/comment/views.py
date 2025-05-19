from rest_framework import viewsets

from comment.models import Comment
from comment.serializers import CommentSerializer
from comment.permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        """
        查看评论允许匿名访问
        创建、编辑和删除评论需要登录
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = []  # 允许匿名访问
        else:
            permission_classes = [IsOwnerOrReadOnly]  # 需要登录且只有评论作者可以编辑
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
