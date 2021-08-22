from django.conf import settings

DEFAULT_KEY = getattr(settings, 'BOOKMARKS_DEFAULT_KEY', 'main')

NEXT_QUERYSTRING_KEY = getattr(settings, 'BOOKMARKS_NEXT_QUERYSTRING', 'next')

DEFAULT_BACKEND = None


