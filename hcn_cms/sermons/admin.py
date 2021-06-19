from .models import Series, Sermon

from django.contrib import admin
import admin_thumbnails

# Register your models here.


@admin.register(Series)
@admin_thumbnails.thumbnail('cover_image')
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'starts_at', 'ends_at', 'tags', 'cover_image_thumbnail']
    search_fields = ['title', 'tags']


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    exclude = ['likes', 'mime_type', 'size']
    list_display = ['title', 'preacher', 'published', 'series', 'url', 'mime_type']
    list_filter = ['preacher', 'series', 'published']
    date_hierarchy = 'published'
    search_fields = ['preacher', 'title', 'series__title']
