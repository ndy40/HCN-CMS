from django.db import models

# Create your models here.


class Series(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    starts_at = models.DateField(null=True)
    ends_at = models.DateField(null=True)
    cover_image = models.ImageField(upload_to='series/%Y/%m/')
    tags = models.JSONField(null=True)


class Sermon(models.Model):
    """
    Model representing sermons. Link to sermin files (mp3 or mp4) is references from url.

    """
    title = models.CharField(max_length=255)
    preacher = models.CharField(max_length=225)
    mime_type = models.CharField(max_length=255)
    url = models.URLField()
    size = models.IntegerField(null=True)
    description = models.TextField(null=True)
    tags = models.JSONField(null=True)
    likes = models.PositiveIntegerField(default=0, null=True)
    published = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='sermons/thumbs/%Y/%m/')
    series = models.ForeignKey('Series', on_delete=models.SET_NULL, null=True)

