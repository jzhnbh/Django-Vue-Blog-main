from rest_framework import serializers
from article.models import Article, Category, CoverImage
from user_info.serializers import UserDescSerializer
from comment.serializers import CommentSerializer
from user_info.models import User

class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    """
    分类序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']

        
class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    coverimage = serializers.ImageField(write_only=True, required=False, allow_null=True)  # 改名
    category_id = serializers.IntegerField(write_only=True),
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Article
        fields = ['id', 'title', 'summary', 'body', 'category', 'category_id', 'coverimage', 'toc', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        coverimage = validated_data.pop('coverimage', None)  # 改名
        category_id = validated_data.pop('category_id')
        validated_data['category'] = Category.objects.get(id=category_id)
        
        validated_data['author'] = User.objects.get(username='jzh')
        
        article = Article.objects.create(**validated_data)
        
        if coverimage:  # 改名
            coverimage_instance = CoverImage.objects.create(content=coverimage)
            article.coverimage = coverimage_instance
            article.save()

        return article


class ArticleSerializer(serializers.ModelSerializer):
    author = UserDescSerializer(read_only=True)
    coverimage_id = serializers.PrimaryKeyRelatedField(
        source='coverimage',
        queryset=CoverImage.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'body',
            'created_at',
            'updated_at',
            'author',
            'category_id',
            'summary',
            'toc',
            'coverimage_id',
            'published'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'coverimage_id' not in data and instance.coverimage:
            data['coverimage_id'] = instance.coverimage.id
        return data

    def create(self, validated_data):
        if 'coverimage' in validated_data:
            validated_data['coverimage'] = validated_data.pop('coverimage')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'coverimage' in validated_data:
            validated_data['coverimage'] = validated_data.pop('coverimage')
        return super().update(instance, validated_data)


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    文章详情序列化器
    """
    comments = CommentSerializer(many=True, read_only=True)
    body_html = serializers.SerializerMethodField()
    toc_html = serializers.SerializerMethodField()
    author = UserDescSerializer(read_only=True)
    coverimage_id = serializers.PrimaryKeyRelatedField(
        source='coverimage',
        queryset=CoverImage.objects.all(),
        required=False,
        allow_null=True
    )

    def get_body_html(self, obj):
        return obj.get_md()[0]
    
    def get_toc_html(self, obj):
        return obj.get_md()[1]
    
    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'body',
            'created_at',
            'updated_at',
            'author',
            'category_id',
            'summary',
            'toc',
            'coverimage_id',
            'published',
            'comments',
            'body_html',
            'toc_html'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'coverimage_id' not in data and instance.coverimage:
            data['coverimage_id'] = instance.coverimage.id
        return data




class CategoryDetailSerializer(serializers.ModelSerializer):
    articles = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'articles']

    def get_articles(self, obj):
        articles = obj.articles.all()
        return ArticleSerializer(articles, many=True).data

class ArticleStatsSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    views_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'created_at', 'likes_count', 'views_count', 'comments_count']