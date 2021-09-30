from admin_thumbnails import thumbnail
from django.contrib import admin

from .models import Preacher, Series, Sermon


# Register your models here.


@admin.register(Series)
@thumbnail('cover_image')
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'starts_at', 'ends_at', 'tags', 'cover_image_thumbnail']
    search_fields = ['title', 'tags']


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    exclude = ['likes', 'mime_type', 'size', 'meta']
    list_display = ['title', 'who_is_preaching', 'published', 'series', 'url', 'mime_type']
    list_filter = ['preacher__name', 'series', 'published']
    date_hierarchy = 'published'
    search_fields = ['preacher__name', 'title', 'series__title']


@admin.register(Preacher)
@thumbnail('image')
class PreacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_thumbnail']
    search_fields = ['name']
