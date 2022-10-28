from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            # 经过有效验证
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            messages.success(request, '图片添加成功')

            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    
    return render(request, 'images/image/create.html', {'section':'images',
                                                        'form': form,
                                                        })


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)

    return render(request, 'images/image/detail.html', {'section': 'images',
                                                        'image':image,
                                                        })
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 21)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # 如果不是整数，返回第一页
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # 如果是ajax请求，又超过了总页数，则返回空
            return HttpResponse('')
        # 不是ajax,又超出了总页数，则返回最后一页
        images = paginator.page(paginator.num_pages)
    
    if request.is_ajax():
        # 是ajax请求，除了第一次请求
        return render(request, 'images/image/list_ajax.html', {'section':'images',
                                                               'images':images,
                                                               })
    # 非ajax请求（第一次请求）
    return render(request, 'images/image/list.html', {'section': 'images',
                                                      'images': images,
                                                      })