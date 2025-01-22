from django.urls import path, include
from .views import down_thread, ThreadDetailView, ThreadListView, redirect_thread

urlpatterns = [
    path('', redirect_thread, name='redirect'),
    path('thread/down', down_thread, name='down'),
    path('thread/<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/list/', ThreadListView.as_view(), name='thread_list'),
]