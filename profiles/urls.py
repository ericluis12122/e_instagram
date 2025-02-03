from django.urls import path

from .views import UserProfileDetailView, UserProfileUpdateView, UserProfilesView, follow_unfollow

urlpatterns = [
    path('<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('update/<int:pk>/', UserProfileUpdateView.as_view(), name='profile_update'),
    path('', UserProfilesView.as_view(), name='profiles'),
    path('follow/<int:user_id>/', follow_unfollow, name='follow_unfollow'),
]