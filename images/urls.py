from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'), # 点赞功能
    
    path('', views.image_list, name='list'),
    # 排名
    path('ranking/', views.image_ranking, name='ranking'),
]