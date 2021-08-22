from django.db import models
from django.contrib.contenttypes.models import ContentType
from .utils import get_content_type_for_model
from .exceptions import AlreadyExist, DoesNotExist


class BookmarkManager(models.Manager):
    """
    Managers used by the Bookmark model
    """
    def get_for(self, content_object, key, **kwargs):
        """
        Return the instance related to *content_object* and matching *kwargs*.
        Return None if a bookmark is not found.

        :param content_object:
        :param key:
        :param kwargs:
        :return:
        """
        content_type = get_content_type_for_model(content_object)
        try:
            return self.get(key=key, content_type=content_type,
                            object_id=content_object.pk, **kwargs)
        except self.model.DoesNotExist:
            return None

    def filter_for(self, content_object_or_model, **kwargs):
        """
        Return all instances related to *content_object_or_model* and matching *kwargs*.
        The argument *content_object_or_model* can be both a model instance or model class.

        :param content_object_or_model:
        :param kwargs:
        :return:
        """
        if isinstance(content_object_or_model, models.base.ModelBase):
            lookups = {'content_type': get_content_type_for_model(content_object_or_model)}
        else:
            lookups = {
                'content_type': get_content_type_for_model(type(content_object_or_model)),
                'object_id': content_object_or_model.pk
            }
        lookups.update(kwargs)
        return self.filter(**lookups)

    def filter_with_content(self, **kwargs):
        """
        Return all instances retrieving content objects in bulk in order
        to minimize db queries, e.g. to get all objects bookmarked by a user::

            for bookmark in Bookmark.objects.filter_with_contents(user=my_user):
                bookmark.content_object # this does not hit the db

        :param kwargs:
        :return:
        """
        if 'content_object' in kwargs:
            content_object = kwargs.pop('content_object')
            query_set = self.filter_for(content_object, **kwargs)
        else:
            query_set = self.filter(**kwargs)

        return query_set

    def add(self, user, content_object, key):
        """
        Add a bookmark, given the user, the model instance and the key.

        Raise a *Bookmark.AlreadyExists* exception if that kind of
        bookmark is present in the db.

        :param user:
        :param content_object:
        :param key:
        :return:
        """
        content_type = get_content_type_for_model(type(content_object))
        try:
            return self.create(user=user, content_type=content_type, object_id=content_object.pk, key=key)
        except Exception:
            raise AlreadyExist

    def remove(self, user, content_object, key):
        """
        Remove a bookmark, given the user, the model instance and the key.

        Raise a *Bookmark.DoesNotExist* exception if that kind of
        bookmark is not present in the db.

        :param user:
        :param content_object:
        :param key:
        :return:
        """
        content_type = get_content_type_for_model(type(content_object))
        try:
            bookmark = self.get(user=user, content_type=content_type, object_id=content_object.pk, key=key)
        except self.model.DoesNotExists:
            raise DoesNotExist

        bookmark.delete()
        return bookmark

    def remove_all_for(self, user, content_object):
        """
        Remove all bookmarks for the given model instance.

        The application uses this whenever a bookmarkable model instance
        is deleted, in order to maintain the integrity of the bookmarks table.

        :param user:
        :param content_object:
        :return:
        """
        content_type = get_content_type_for_model(type(content_object))
        self.filter(content_type=content_type, object_id=content_object.id).delete()
