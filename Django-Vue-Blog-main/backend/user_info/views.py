from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from user_info.models import User, AuthInfo
from user_info.serializers import (
    UserRegisterSerializer,
    UserDetailSerializer,
    UserDescSerializer,
    AuthInfoSerializer
)
from user_info.permissions import IsSelfOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly, IsSelfOrReadOnly]

        return super().get_permissions()
    
    @action(detail=True, methods=['get'])
    def info(self, request, username=None):
        queryset = User.objects.get(username=username)
        serializer = UserDetailSerializer(queryset, many=False)
        return Response(serializer.data)
    
    @action(detail=False)
    def sorted(self, reqeust):
        users = User.objects.all().order_by('-username')
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        
        if user is None or not user.check_password(password):
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class AuthInfoViewSet(viewsets.ModelViewSet):
    queryset = AuthInfo.objects.all()
    serializer_class = AuthInfoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
