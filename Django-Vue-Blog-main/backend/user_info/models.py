from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    description = models.CharField(max_length=500, blank=True)
    avatar = models.ForeignKey(
        'article.CoverImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user_avatar'
    )

    def __str__(self):
        return self.username

class AuthInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_info')
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.token}'
