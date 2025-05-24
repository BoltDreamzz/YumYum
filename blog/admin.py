from django.contrib import admin

# Register your models here.
from .models import Blog, BlogSlugHistory

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    readonly_fields = ('slug',)

@admin.register(BlogSlugHistory)
class BlogSlugHistoryAdmin(admin.ModelAdmin):
    list_display = ('old_slug', 'blog')