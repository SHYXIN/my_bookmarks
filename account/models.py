from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE,
                                )
    
    date_of_birth = models.DateTimeField(verbose_name='出生日期', blank=True, null=True, )
    photo = models.ImageField(verbose_name='图片', upload_to='users/%Y/%m/%d/', blank=True)
    
    class Meta:
        verbose_name = 'Profile-用户简介'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f'{self.user.username}的简介'