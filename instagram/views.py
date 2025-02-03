from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm
from .forms import RegisterForm
from profiles.models import UserProfile, Follow
from posts.models import Post

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=self.request.user)

            following_profiles = Follow.objects.filter(follower=user_profile).values_list('following', flat=True)

            if following_profiles.exists():
                context['posts'] = Post.objects.filter(user__profile__in=following_profiles).order_by('-created_at')[:5]
            else:
                context['posts'] = Post.objects.none()
        else:
            context['posts'] = Post.objects.all().order_by('-created_at')[:5]

        return context


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm 

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "Login successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User created successfully!')
        return response
    

class ContactView(TemplateView):
    template_name = 'contact.html'