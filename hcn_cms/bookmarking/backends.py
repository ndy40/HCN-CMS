from importlib import import_module

from django.db import transaction

from .models import Bookmark
from .exceptions import DoesNotExists
from .utils import get_content_type_for_model


class BaseBackend(object):
    """
    Base bookmarks backend.

    Users may want to change *settings.GENERIC_BOOKMARKS_BACKEND*
    and customize the backend implementing all the methods defined here.
    """
    def get_model(self):
        """
        Must return the bookmark model (a Django model or anything you like).
        Instances of this model must have the following attributes:

            - user (who made the bookmark, a Django user instance)
            - key (the bookmark key, as string)
            - content_type (a Django content_type instance)
            - object_id (a pk for the bookmarked object)
            - content_object (the bookmarked object as a Django model instance)
            - created_at (the date when the bookmark is created)
        """
        raise NotImplementedError

    def add(self, user, instance, key):
        """
        Must create a bookmark for *instance* by *user* using *key*.
        Must return the created bookmark (as a *self.get_model()* instance).
        Must raise *exceptions.AlreadyExists* if the bookmark already exists.
        """
        raise NotImplementedError

    def remove(self, user, instance, key):
        """
        Must remove the bookmark identified by *user*, *instance* and *key*.
        Must return the removed bookmark (as a *self.get_model()* instance).
        Must raise *exceptions.DoesNotExist* if the bookmark does not exist.
        """
        raise NotImplementedError

    def remove_all_for(self, instance):
        """
        Must delete all the bookmarks related to given *instance*.
        """
        raise NotImplementedError

    def filter(self, **kwargs):
        """
        Must return all bookmarks corresponding to given *kwargs*.
        The *kwargs* keys can be:
            - user: Django user object or pk
            - instance: a Django model instance
            - content_type: a Django ContentType instance or pk
            - model: a Django model
            - key: the bookmark key to use
            - reversed: reverse the order of results
        The bookmarks must be an iterable (like a Django queryset) of
        *self.get_model()* instances.
        The bookmarks must be ordered by creation date (*created_at*):
        if *reversed* is True the order must be descending.
        """
        raise NotImplementedError

    def get(self, user, instance, key):
        """
        Must return a bookmark added by *user* for *instance* using *key*.
        Must raise *exceptions.DoesNotExist* if the bookmark does not exist.
        """
        raise NotImplementedError

    def exists(self, user, instance, key):
        """
        Must return True if a bookmark given by *user* for *instance*
        using *key* exists, False otherwise.
        """
        raise NotImplementedError


class ModelBackend(BaseBackend):
    """
    Bookmarks backend based on Django models.
    This is used by default if no other backend is specified.
    """

    def get_model(self):
        return Bookmark

    @transaction.atomic
    def add(self, user, instance, key):
        return self.get_model().objects.add(user=user, content_object=instance, key=key)

    @transaction.atomic
    def remove(self, user, instance, key):
        return self.get_model().objects.remove(user=user, content_object=instance, key=key)

    @transaction.atomic
    def remove_all_for(self, instance):
        return self.get_model().objects.remove_all_for(content_object=instance)

    def filter(self, **kwargs):
        """
        The *kwargs* can be:
            - user: Django user object or pk
            - instance: a Django model instance
            - content_type: a Django ContentType instance or pk
            - model: a Django model
            - key: the bookmark key to use
            - reversed: reverse the order of results
        """
        order = '-created_at' if kwargs.pop('reversed', False) else 'created_at'
        if 'instance' in kwargs:
            instance = kwargs.pop('instance')
            kwargs.update({
                'content_type': get_content_type_for_model(instance),
                'object_id': instance.pk
            })
        elif 'model' in kwargs:
            model = kwargs.pop('model')
            kwargs['content_type'] = get_content_type_for_model(model)

        if 'user' in kwargs:
            query_set = self.get_model().objects.filter_with_content(**kwargs)
        else:
            query_set = self.get_model().objects.filter(**kwargs)
        return query_set.order_by(order)

    def get(self, user, instance, key):
        bookmark = self.get_model().objects.get_for(content_object=instance, key=key, user=user)
        if bookmark is None:
            raise DoesNotExists

        return bookmark

    def exists(self, user, instance, key):
        return self.filter(instance=instance, user=user, key=key).exists()


def get_backend():
    return ModelBackend()


def get_model():
    return Bookmark
