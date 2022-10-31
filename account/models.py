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
    
class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)  # 创建{关注}关系的人
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set',on_delete=models.CASCADE)  # 被关注的人
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='关注时间')
    
    class Meta:
        ordering = ('created', )
    
    def __str__(self):
        return f'{self.user_from}关注了{self.user_to}'
    

# 动态增加User follow的字段
#  user.followers.all() and user.following.all().
from django.contrib.auth import get_user_model
user_model = get_user_model()
user_model.add_to_class('following',   # 增加的字段名
                        models.ManyToManyField('self', 
                                               through=Contact, 
                                               related_name='followers', 
                                               symmetrical=False,  # 不对称
                                               verbose_name='跟随者',
                                               ))