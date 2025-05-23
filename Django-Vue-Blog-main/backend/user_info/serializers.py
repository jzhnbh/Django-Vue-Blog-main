from user_info.models import User, AuthInfo
from rest_framework import serializers


class UserDescSerializer(serializers.ModelSerializer):
    """
    文章列表中引用的嵌套用户信息
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'avatar'
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户管理序列化器
    """
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'password', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'last_login',
            'date_joined',
            'avatar',
            'is_superuser'
        ]

class AuthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthInfo
        fields = ['id', 'user', 'token', 'created_at', 'updated_at']
