from django.dispatch import Signal

bookmark_pre_save = Signal(providing_args=['form', 'requests'])

bookmark_post_save = Signal(providing_args=['bookmark', 'request', 'created'])
