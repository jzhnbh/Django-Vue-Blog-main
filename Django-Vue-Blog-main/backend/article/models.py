from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from markdown import Markdown
from django.conf import settings


class CoverImage(models.Model):
    """
    文章封面图
    """
    content = models.ImageField(upload_to='coverimage/%Y%m%d')

    def __str__(self):
        return f"CoverImage {self.id}"


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


# class User(AbstractUser):
#     full_name = models.CharField(max_length=255, blank=True, null=True)
#     avatar = models.ForeignKey('Avatar', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
#     role = models.CharField(max_length=50, default='user')
#     first_name = models.CharField(max_length=150, blank=True, null=True)
#     last_name = models.CharField(max_length=150, blank=True, null=True)


class Article(models.Model):
    """
    博客文章
    """
    title = models.CharField(max_length=255)
    summary = models.TextField()
    body = models.TextField()
    coverimage = models.ForeignKey(
        CoverImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    author = models.ForeignKey(
        'user_info.User',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    toc = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title
    
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)

        return md_body, md.toc

    @property
    def likes_count(self):
        return self.articlelike_set.count()

    @property
    def views_count(self):
        return self.articleview_set.count()
    
    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey('user_info.User', on_delete=models.CASCADE, related_name='article_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"


class ArticleView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey('user_info.User', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
