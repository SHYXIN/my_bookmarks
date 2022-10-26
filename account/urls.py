
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('login/', views.user_login, name='login'),
    
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # # 修改密码
    # path('password_change/',auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # # 重置密码
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # django自带的
    path('', include('django.contrib.auth.urls')),
    
    # 注册
    path('register/', views.register, name='register'),
    
    # 用户编辑信息
    path('edit/', views.edit, name='edit')    
]