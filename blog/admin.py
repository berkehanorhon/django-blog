import logging

from django.contrib import admin
from django.db.models import Q
from django.utils.timezone import now

from .models import BlogPost, Category
from .views import send_newpost_email_to_subscribers

logger = logging.getLogger(__name__)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'isPublished', 'publish_date')
    list_filter = ('author', 'category', 'isPublished')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 50
    actions = ('make_published',)

    def make_published(self, request, queryset):
        count = queryset.update(isPublished=True)
        for post in queryset.filter(Q(publish_date__isnull=True)):
            try:
                logging.info(f'Publishing post {post.id}')
                send_newpost_email_to_subscribers(post.slug)
            except:
                logging.error(f'Email sending failed for post {post.id}')
        queryset.update(publish_date=now())
        self.message_user(request, f'{count} blog posts have been published.')

    make_published.short_description = 'Publish selected blog posts'


admin.site.register(Category)
