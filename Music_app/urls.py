from django.urls import path
from Music_app.views import homepage, register, upload_file, user_login, logout_view
from . import views

app_name = 'Music_app'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_file, name='upload_file'),
]



