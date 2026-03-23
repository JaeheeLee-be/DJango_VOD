from django.urls import path
from . import views, cb_views

urlpatterns = [
    # FBV
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/<int:todo_id>/', views.todo_info, name='todo_info'),
    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/<int:todo_id>/update/', views.todo_update, name='todo_update'),
    path('todo/<int:todo_id>/delete/', views.todo_delete, name='todo_delete'),
]