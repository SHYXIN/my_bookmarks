from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

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
    return render(request, 'account/dashboard.html', {'section' : 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)   # 创建用户但未提交
            new_user.set_password(user_form.cleaned_data['password'])  # 设置所选密码
            new_user.save() # Save the User object
            # 创建Profile
            Profile.objects.create(user=new_user)
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

