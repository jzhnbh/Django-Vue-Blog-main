from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        # 允许管理员编辑所有用户
        if request.user.is_superuser:
            return True
            
        # 普通用户只能编辑自己
        return obj == request.user
    