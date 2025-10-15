from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post
from marketplace.models import Service
from academy.models import LearningPathway


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return [
            'core:home', 
            'core:terms', 
            'core:privacy', 
            'marketplace:service-list', 
            'blog:post_list', 
            'academy:home'
        ]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish')

    def lastmod(self, obj):
        return obj.updated


class ServiceSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.6

    def items(self):
        return Service.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse('marketplace:service-detail', kwargs={'pk': obj.pk})


class ArtisanProfileSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return User.objects.filter(profile__is_verified_artisan=True)

    def location(self, obj):
        return reverse('users:artisan-storefront', kwargs={'username': obj.username})


class LearningPathwaySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # 🚀 THE ONLY FIX NEEDED IS ON THIS LINE 🚀
        # Removed the filter for 'is_public=True' which does not exist on the LearningPathway model.
        return LearningPathway.objects.all().order_by('-created_at')

    def location(self, obj):
        # This correctly points to the public detail view for each pathway.
        return reverse('academy:public-pathway-detail', kwargs={'pk': obj.pk})

    def lastmod(self, obj):
        return obj.created_at
