from django.urls import path

from .views import PostCreateView, PostDetailView, post_like

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    #path('edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    #path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/like/', post_like, name='post_like'),
]