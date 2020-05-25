from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category, Tag
from .forms import PostForm


class PostAdmin(admin.ModelAdmin):

    form = PostForm
    exclude = ('view_count', )
    filter_horizontal = ('categories', 'tags')
    list_display = ('title', 'thumbnail_preview',
                    'overview', 'is_public', 'view_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_filter = ('is_public',)
    search_fields = ('title', 'overview', 'content')

    def thumbnail_preview(self, obj):
        return mark_safe('<img src="{}" style="width:100px; height:auto;">'.format(obj.thumbnail.url))

    thumbnail_preview.short_description = 'Preview'


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
