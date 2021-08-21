import json

from django.db.models.signals import pre_delete
from django.db.models.base import ModelBase

from .settings import DEFAULT_KEY
from .backends import get_backend
from .signals import bookmark_pre_save, bookmark_post_save
from .exceptions import AlreadyHandled, NotHandled


class Handler(object):
    default_key = 'main'
    allowed_keys = [DEFAULT_KEY]

    def __init__(self, model, backend):
        self.model = model
        self.backend = backend

    def __getattr__(self, attr):
        if attr in ('get', 'filter', 'exists'):
            return getattr(self.backend, attr)
        return AttributeError

    def get_key(self, request, instance, key=None):
        return key or self.default_key

    def allow_key(self, request, instance, key):
        return key in self.allow_key

    def fail(self, request, errors):
        """
        Callback used by the bookmarking views, called when bookmark form
        did not validate. Must return a Django http response.
        """
        from django.http import HttpResponseBadRequest
        return HttpResponseBadRequest(self.failure_message)

    # receivers

    def remove_all_for(self, sender, instance, **kwargs):
        """
        The target object *instance* of the model *sender*, is being deleted,
        so we must delete all the bookmarks related to that instance.

        This receiver is usually connected by the bookmark registry, when
        a handler is registered.
        """
        self.backend.remove_all_for(instance)


class Registry(object):
    def __init__(self):
        self._registry = {}
        self.backend = get_backend()
        self._connect(self.backend.get_model())

    def _connect(self, model):
        bookmark_pre_save.connect(self._pre_save, sender=model)
        bookmark_post_save.connect(self._post_save, sender=model)

    def _connect_model_signals(self, model, handler):
        pre_delete.connect(handler.remove_all_for, sender=model)

    def _get_handler_instance(self, model, handler_class, options):
        handler = handler_class(model, self.backend)

        for k, v in options.items():
            setattr(handler, k, v)

        return handler

    def register(self, model_or_iterable, handler_class=None, **kwargs):
        if handler_class is None:
            handler_class = Handler

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyHandled(
                    "The model '%s' is already being handled" %
                    model._meta.module_name
                )
            handler = self._get_handler_instance(model, handler_class, kwargs)
            self._registry[model] = handler
            self._connect_model_signals(model, handler)

    def unregister(self, model_or_iterable):
        """
        Remove a model or list of models from the list of models that will be handled
        :param model_or_iterable:
        :return:
        :raise NotHandled
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]

        for model in model_or_iterable:
            if model not in self._registry:
                raise NotHandled(
                    "The model '%s' is not currently being handled" %
                    model._meta.module_name
                )
            del self._registry[model]

    def get_handler(self, model_or_instance):
        """
        Return the handler for given model or model instance.
        Return None if model is not registered.
        """
        if isinstance(model_or_instance, ModelBase):
            model = model_or_instance
        else:
            model = type(model_or_instance)
        return self._registry.get(model)

    def _pre_save(self, sender, form, request, **kwargs):
        """
        Apply any necessary pre-save steps to bookmarks.
        """
        model = type(form.instance())
        if model in self._registry:
            return self._registry[model].pre_save(request, form)
        return False

    def _post_save(self, sender, bookmark, request, created, **kwargs):
        """
        Apply any necessary post-save steps to new bookmarks.
        """
        model = bookmark.content_type.model_class()
        if model in self._registry:
            return self._registry[model].post_save(request, bookmark, created)


library = Registry()
