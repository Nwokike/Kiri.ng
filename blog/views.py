from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Post, Comment
from .forms import PostForm, CommentForm
from notifications.models import Notification  # Added import


class PostListView(generic.ListView):
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
        category = self.request.GET.get('category')
        if category and category in dict(Post.Category.choices):
            queryset = queryset.filter(category=category)
        return queryset


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs['post'],
            publish__year=self.kwargs['year'],
            publish__month=self.kwargs['month'],
            publish__day=self.kwargs['day']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # --- CREATE NOTIFICATION ---
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    message=_(f"{request.user.username} commented on your post: '{post.title}'"),
                    link=post.get_absolute_url()
                )

            messages.success(request, _("Your comment has been added."))
            return redirect(post.get_absolute_url())

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('marketplace:artisan-dashboard')

    def test_func(self):
        return self.request.user.profile.is_verified_artisan

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, _("Your post has been saved as a draft."))
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        messages.success(self.request, _("Your post has been updated successfully."))
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def post(self, request, *args, **kwargs):
        messages.success(self.request, _("Your comment has been deleted."))
        return super().post(request, *args, **kwargs)
