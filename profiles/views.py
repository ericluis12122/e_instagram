from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from .models import UserProfile, Follow
from posts.models import Post

# Create your views here.
@login_required
def follow_unfollow(request, user_id):
    # Obtén el perfil de usuario al que se quiere seguir o dejar de seguir
    target_profile = get_object_or_404(UserProfile, user__id=user_id)
    # Obtén el perfil del usuario actual
    current_profile = request.user.profile

    # Si el usuario intenta seguirse a sí mismo, no se permite
    if target_profile == current_profile:
        return HttpResponseForbidden("You cannot follow yourself.")

    # Verifica si el usuario ya sigue al objetivo
    follow_exists = Follow.objects.filter(follower=current_profile, following=target_profile).exists()

    if follow_exists:
        # Si el usuario ya sigue al objetivo, deja de seguirlo
        Follow.objects.filter(follower=current_profile, following=target_profile).delete()
    else:
        # Si no lo sigue, entonces lo sigue
        Follow.objects.create(follower=current_profile, following=target_profile)

    return redirect('profile_detail', pk=target_profile.pk)

class UserProfilesView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = "profile_list.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = UserProfile.objects.all().exclude(user=self.request.user)
        return context

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "profile_detail.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['posts'] = Post.objects.filter(user=user_profile.user).order_by('-created_at')
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = "profile_update.html"
    fields = ['profile_picture', 'bio', 'birth_date']
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Update successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Update failed. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.get_object().pk}) 
    
    def dispatch(self, request, *args, **kwargs):
        profile = self.get_object()
        if profile.user != request.user:
            return HttpResponseForbidden("Do not have permission to edit this profile.")
        return super().dispatch(request, *args, **kwargs)