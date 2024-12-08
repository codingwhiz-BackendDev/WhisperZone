from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name= 'index'),
    path('register', views.register, name= 'register'),
    path('login', views.login, name= 'login'),
    path('logout', views.logout, name= 'logout'),
    path('view_messages', views.view_messages, name= 'view_messages'),
    path('send_message/<str:pk>', views.send_message, name= 'send_message'),
    path('view_secret_link/<str:pk>', views.view_secret_link, name= 'view_secret_link'),
]
