from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from actions.models import Action

from actions.utils import create_action
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Profile, Contact
from django.contrib import messages
from django.contrib.auth.models import User
from common.decorators import ajax_required
# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password']
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('登陆成功')
                else:
                    return HttpResponse('账户已禁用')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    
    
    return render(request, 'account/login.html', {'form':form,
                                                  })
    

@login_required
def dashboard(request):
    # 默认情况下，显示所有action
    actions = Action.objects.exclude(user=request.user)  # 排除自己的动作

    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        # 如果用户正在跟踪其他人，则只检索他们的操作
        actions = actions.filter(user_id__in=following_ids)

    # actions = actions[:10]
    # actions = actions.select_related('user', 'user__profile')[:10]  # sql优化
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    
    
    return render(request, 'account/dashboard.html', {'section' : 'dashboard',
                                                      'actions':actions,
                                                      })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)   # 创建用户但未提交
            new_user.set_password(user_form.cleaned_data['password'])  # 设置所选密码
            new_user.save() # Save the User object
            # 创建Profile
            Profile.objects.create(user=new_user)
            create_action(request.user, '新建了账号')
            return render(request, 'account/register_done.html', {'new_user': new_user})
        
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {'user_form': user_form,
                                                     })
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                       data=request.POST,
                                       files=request.FILES,  # 图片
                                       )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '编辑信息成功')
        else:
            messages.error(request, '编辑信息发生错误')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form,
                                                 })

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    # print([i.profile for i in users])
    return render(request, 'account/user/list.html', {'section':'people',
                                                      'users':users,
                                                      })

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)

    return render(request, 'account/user/detail.html', {'section': 'people',
                                                        'user':user,
                                                        })

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                # 创建关系
                Contact.objects.get_or_create(
                    user_from = request.user,
                    user_to = user,
                    )
                create_action(request.user, '关注了', user)
            else:
                # 删除关系
                Contact.objects.filter(user_from=request.user,
                                       user_to=user,
                                       ).delete()
            return JsonResponse({'status':'ok'})
        except User.DoseNotexist:
            return JsonResponse({'status': 'error'})
    
    return JsonResponse({'status': 'error'})
    

