from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .manager import BookmarkManager

# Create your models here.


class Bookmark(models.Model):
    """
    Model for holding bookmarking of models by the user e.g Video, Series, Sermons etc.

    .. py:attribute:: content_type
        the bookmarked instance of content type
    .. py:attribute:: object_id
        the id of the model
    .. py:attribute:: content_object
        the bookmarked instance
    .. py:attribute:: key
        the bookmark key
    .. py:attribute:: created_at
        The date bookmark was created.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    key = models.CharField(max_length=16)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='bookmarks',
                             on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    # managers
    objects = BookmarkManager()

    class Meta:
        unique_together = ('content_type', 'object_id', 'key', 'user')

    def __unicode__(self):
        return u'Bookmark for %s by %s' % (self.content_object, self.user)
