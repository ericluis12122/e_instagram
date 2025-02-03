from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Comment
from .forms import CommentForm

# Create your views here.
@login_required
@require_POST
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    # Si el usuario ya le dio like, lo quitamos
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        # Si el usuario no le ha dado like, lo agregamos
        post.likes.add(request.user)
        liked = True

    # Retornar el nuevo número de likes y si el usuario lo ha dado like o no
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['is_owner'] = post.user == self.request.user
        context['form'] = CommentForm()
        context['comments'] = post.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(request.path)
        return self.get(request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['image', 'caption']
    template_name = 'post_form.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
