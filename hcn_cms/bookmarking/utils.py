from django.contrib.contenttypes.models import ContentType
from functools import cache


@cache
def get_content_type_for_model(model):
    return ContentType.objects.get_for_model(model)
