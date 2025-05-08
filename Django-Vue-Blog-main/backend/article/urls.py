from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article import views

router = DefaultRouter()
router.register(r'article', views.ArticleViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'coverimage', views.CoverImageViewSet)

urlpatterns = [
    path('article/stats/', views.article_stats, name='article-stats'),
    path('article/<int:pk>/comments/', views.article_comments, name='article-comments'),
    path('article/update_meta/<int:pk>/', views.ArticleMetaUpdateView.as_view(), name='article-meta-update'),
    path('article/<int:pk>/like/', views.article_like, name='article-like'),
    path('', include(router.urls)),
]
