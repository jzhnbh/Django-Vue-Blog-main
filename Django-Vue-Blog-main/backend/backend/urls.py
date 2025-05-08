from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from article import views
from comment.views import CommentViewSet
from user_info.views import UserViewSet, LoginView, AuthInfoViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# 创建路由器
router = DefaultRouter()
# 移除这些路由注册，因为它们已经在 article/urls.py 中注册了
# router.register(r'article', views.ArticleViewSet)
# router.register(r'category', views.CategoryViewSet)
# router.register(r'coverimage', views.CoverImageViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'user', UserViewSet)
router.register(r'auth-info', AuthInfoViewSet)

# API 文档配置
schema_view = get_schema_view(
   openapi.Info(
      title="Blog API",
      default_version='v1',
      description="博客系统API文档",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', LoginView.as_view(), name='login'),
    
    # swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('article.urls')),  # 改回来
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
