# your_app/urls.py
from django.urls import path
from . import views

app_name = 'chatai' # 建议添加 app_name

urlpatterns = [
    path('', views.chat_view, name='index'), # 聊天页面 URL
    path('send_message/', views.send_message_view, name='send_message'), # 处理消息的 URL
]