from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Video, Category, TaggedItem


class TaggedItemInline(GenericTabularInline):
	model = TaggedItem


class VideoInline(admin.TabularInline):
	model = Video


class VideoAdmin(admin.ModelAdmin):
	inlines = [TaggedItemInline]
	list_display = ["title", 'slug']
	fields = ['title', 'order', 'share_message', 'embed_code','active','slug',
			'featured', 'free_preview', 'category']
	prepopulated_fields = {'slug': ["title"]}


class CategoryAdmin(admin.ModelAdmin):
	inlines = [VideoInline, TaggedItemInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Video, VideoAdmin)
