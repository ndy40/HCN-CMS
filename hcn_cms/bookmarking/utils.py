from functools import cache

from django.contrib.contenttypes.models import ContentType


@cache
def get_content_type_for_model(model):
    return ContentType.objects.get_for_model(model)
