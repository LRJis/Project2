from django.urls import path
from .import views

app_name = 'blog'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('private/<int:pk>/', views.private, name='private'),
    path('add_private/<int:pk>', views.add_private, name='add_private'),
    path('look_article/<int:pk>', views.look_article, name='look_article'),
    path('look_user/<int:pk>', views.look_user, name='look_user'),
    path('logout/', views.logout, name='logout'),
    path('edit_article/<int:pk>', views.edit_article, name='edit_article'),
    path('send_message/<int:pk>', views.send_message, name='send_message'),
    path('check_message/<int:pk>', views.check_message, name='check_message'),
    path('check_one/<int:pk>', views.check_one, name='check_one'),
    path('add_file/<int:pk>', views.add_file, name='add_file'),
    path('check_files/<int:pk>', views.check_files, name='check_files'),
    path('check_file/<int:pk>', views.check_file, name='check_file'),
]
