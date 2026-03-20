from django.urls import path

from blog import views

app_name = 'fb'

urlpatterns = [
    # FBV blog
    path('', views.blog_list, name='list'),
    path('<int:pk>/', views.blog_detail, name='detail'),
    path('create/', views.blog_create, name='create'),
    path('<int:pk>/update', views.blog_update, name='update'),

]