from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.PageCreateView.as_view(), name='create'),
    path('list/', views.PageListView.as_view(), name='list'),
    path('detail/<int:id>', views.PageDetailView.as_view(), name='detail'),
    path('edit/<int:id>', views.PageEditView.as_view(), name='edit'),
    path('delete/<int:id>', views.PageDeleteView.as_view(), name='delete'),
]

