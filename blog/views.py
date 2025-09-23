from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from .forms import PostForm # <-- Import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

class PostListView(generic.ListView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Post,
                                 status=Post.Status.PUBLISHED,
                                 slug=self.kwargs['post'],
                                 publish__year=self.kwargs['year'],
                                 publish__month=self.kwargs['month'],
                                 publish__day=self.kwargs['day'])

# --- THIS IS THE NEW VIEW ---
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')

    def test_func(self):
        # Only verified artisans can create a post
        return self.request.user.profile.is_verified_artisan

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Your post has been saved as a draft. It will be reviewed by an admin before publishing."))
        return super().form_valid(form)