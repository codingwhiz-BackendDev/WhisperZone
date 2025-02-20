from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('register', views.register, name= 'register'),
    path('login', views.login, name= 'login'),
    path('logout', views.logout, name= 'logout'),
    path('accounts/', include('allauth.urls')),
    path('view_messages', views.view_messages, name= 'view_messages'),
    path('send_message/<str:pk>', views.send_message, name= 'send_message'),
    path('view_secret_link/<str:pk>', views.view_secret_link, name= 'view_secret_link'),
    path('profile/<str:pk>', views.profile, name= 'profile'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('delete_poll/<str:pk>', views.delete_poll, name='delete_poll'),
    path('social_media/<str:pk>', views.social_media, name='social_media'),
    path('make_message_private', views.make_message_private, name='make_message_private'),
    path('public_messages/<str:pk>', views.public_messages, name='public_messages'),
    path('create_poll', views.create_poll, name='poll'),
    path('poll/<str:pk>', views.poll, name='poll'),
    path('view_poll/<str:pk>/<str:question>', views.view_poll, name='view_poll'),
    path('vote/<str:pk>',views.vote, name='vote' ),
    path('like_message/<str:pk>', views.like_message, name='like_message'),
    
    
    # Forgot Password URLS
    path('forgot_password/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='forgot_password'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
