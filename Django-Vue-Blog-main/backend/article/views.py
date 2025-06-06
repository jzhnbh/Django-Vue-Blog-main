from rest_framework import viewsets
from rest_framework import filters as rest_filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework import generics
from rest_framework import status
from django.db.models import Count

from article.permissions import IsAdminUserOrReadOnly
from article.models import Article, Category, CoverImage, ArticleLike
from user_info.models import User
from article.serializers import (
    ArticleSerializer,
    CategorySerializer,
    CoverImageSerializer,
    CategoryDetailSerializer,
    ArticleDetailSerializer,
    ArticleStatsSerializer,
    CommentSerializer,
)

# 添加过滤器类
class ArticleFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category')
    
    class Meta:
        model = Article
        fields = ['category']

class CoverImageViewSet(viewsets.ModelViewSet):
    """
    文章封面图视图集
    """
    queryset = CoverImage.objects.all()
    serializer_class = CoverImageSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    分类视图集
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer
        
    @action(detail=True, methods=['get'])
    def articles(self, request, pk=None):
        """获取特定分类下的所有文章"""
        category = self.get_object()
        articles = Article.objects.filter(category=category)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

class ArticleViewSet(viewsets.ModelViewSet):
    """
    文章的增删改查接口
    
    list:
    获取文章列表
    * 支持按分类过滤
    * 支持标题搜索
    
    create:
    创建新文章
    * 必须提供标题和内容
    * 可选提供封面图
    
    retrieve:
    获取文章详情
    * 包含完整的文章内容和评论
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        """
        获取文章列表和详情允许匿名访问
        创建、编辑和删除需要管理员权限
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = []  # 允许匿名访问
        else:
            permission_classes = [IsAuthenticated]  # 需要登录
        return [permission() for permission in permission_classes]

    filter_backends = [rest_filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = ArticleFilter
    search_fields = ['title']

    def get_queryset(self):
        """
        支持通过 category 参数过滤文章
        ?category=1 获取分类ID为1的文章
        """
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset

    def perform_create(self, serializer):
        # 确保处理category_id
        category_id = self.request.data.get('category_id')
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
                
        # 如果前端没有传递 author，则默认设置为 jzh
        if 'author' not in serializer.validated_data:
            user = User.objects.get(username='jzh')  # 假设用户名为 jzh
            serializer.save(author=user, category=category)
        else:
            serializer.save(category=category)
            
    def perform_update(self, serializer):
        # 确保处理category_id
        category_id = self.request.data.get('category_id')
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
                
        serializer.save(category=category)
            
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

    @action(detail=True, methods=['GET'])
    def comments(self, request, pk=None):
        article = self.get_object()
        comments = article.comments.all()
        serializer = CommentSerializer(
            comments, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

class ArticleMetaUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated]  # 保持需要登录权限
    
    def update(self, request, *args, **kwargs):
        article = self.get_object()
        
        # 只更新标题和分类
        title = request.data.get('title')
        category_id = request.data.get('category_id')
        
        if title is not None:
            article.title = title
        if category_id is not None:
            try:
                category = Category.objects.get(id=category_id)
                article.category = category
            except Category.DoesNotExist:
                return Response(
                    {"error": "Category not found"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        article.save()
        return Response({"message": "Updated successfully"})

@api_view(['GET'])
# 管理员才能访问统计信息
@permission_classes([IsAuthenticated])
def article_stats(request):
    # 检查是否是管理员
    if not request.user.is_superuser:
        return Response({'error': '只有管理员可以访问此功能'}, status=403)
            
    try:
        articles = Article.objects.annotate(
            likes_count=Count('articlelike'),
            views_count=Count('articleview'),
            comments_count=Count('comments')
        ).values(
            'id', 
            'title', 
            'created_at',
            'likes_count',
            'views_count',
            'comments_count'
        ).order_by('-created_at')
                
        return Response(list(articles))
    except Exception as e:
        return Response(
            {'error': f'获取文章统计失败: {str(e)}'}, 
            status=500
        )

@api_view(['GET'])
# 允许匿名查看评论
def article_comments(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        comments = article.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except Article.DoesNotExist:
        return Response({'error': '文章不存在'}, status=404)

@api_view(['GET', 'POST', 'DELETE'])
def article_like(request, pk):
    try:
        article = Article.objects.get(pk=pk)
               
        if request.method == 'GET':
            # 获取点赞数量不需要登录
            like_count = ArticleLike.objects.filter(article=article).count()
                       
            # 检查用户是否已点赞（需要登录）
            is_liked = False
            if request.user.is_authenticated:
                is_liked = ArticleLike.objects.filter(
                    article=article,
                    user=request.user
                ).exists()
                           
            return Response({
                'is_liked': is_liked,
                'like_count': like_count
            })
                   
        elif not request.user.is_authenticated:
            return Response({'error': '请先登录'}, status=401)
                   
        elif request.method == 'POST':
            # 添加点赞
            ArticleLike.objects.get_or_create(
                article=article,
                user=request.user
            )
            return Response({'status': 'liked'})
                   
        elif request.method == 'DELETE':
            # 取消点赞
            ArticleLike.objects.filter(
                article=article,
                user=request.user
            ).delete()
            return Response({'status': 'unliked'})
               
    except Article.DoesNotExist:
        return Response({'error': '文章不存在'}, status=404)