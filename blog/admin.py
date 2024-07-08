from django.contrib import admin

from .models import BlogPost, Category
from django.utils.timezone import now

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'isPublished', 'publish_date')
    list_filter = ('author', 'category', 'isPublished')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 50
    actions = ('make_published',)

    def make_published(self, request, queryset):
        count = queryset.update(isPublished=True)
        queryset.update(publish_date=now())
        self.message_user(request, f'{count} blog posts have been published.')
    make_published.short_description = 'Publish selected blog posts'
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Category)
