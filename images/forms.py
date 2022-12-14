from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }
    
    def clear_url(self):
        """验证表单上传的是不是规定格式"""
        url = self.cleaned_data['url']
        valid_extension = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extension:
            raise forms.ValidationError('URL不是jpg或者jpeg格式')
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        """重写save方法"""
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image.url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # 从给定的url中下载图片
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)
        
        if commit:
            image.save()        
        return image