from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Comment #<-- Import Comment
from .forms import PostForm, CommentForm #<-- Import CommentForm
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
        return get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=self.kwargs['post'], publish__year=self.kwargs['year'], publish__month=self.kwargs['month'], publish__day=self.kwargs['day'])

    def get_context_data(self, **kwargs):
        # --- This logic adds comments to the page ---
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        # --- This logic handles submitting a new comment ---
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, _("Your comment has been added."))
            return redirect(post.get_absolute_url())
        else:
            context = self.get_context_data()
            context['comment_form'] = form
            return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')
    def test_func(self): return self.request.user.profile.is_verified_artisan
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Your post has been saved as a draft."))
        return super().form_valid(form)