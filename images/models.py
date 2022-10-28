from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='image_created',
                             on_delete=models.CASCADE,
                             verbose_name='用户',
                             )
    title = models.CharField(max_length=200, verbose_name='标题',)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d',)
    description = models.TextField(blank=True, verbose_name='描述', )
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间', )

    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='image_liked',
                                        blank=True
                                        )
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])