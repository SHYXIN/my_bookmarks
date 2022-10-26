"""让我们创建一个身份验证后端来让用户进行身份验证在您的网站中使用他们的电子邮件地址而不是他们的用户名。"""
from django.contrib.auth.models import User

class EmailAuthBackend(object):
    """
    通过邮箱地址进行认证，登录方式
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    def get_user(user, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    