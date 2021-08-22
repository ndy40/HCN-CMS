from accounts.models import User
from bookmarking.exceptions import AlreadyExist
from bookmarking.handlers import library


def increment_like_on_model(*, instance, user: User):
    existing_bookmark = library.backend.filter(instance=instance, user=user)

    if not existing_bookmark.exists():
        library.backend.add(user, instance, 'like')
        if hasattr(existing_bookmark, 'likes'):
            instance.likes += 1
            instance.save()

    raise AlreadyExist(f'{type(instance)} {instance.id} already bookmarked')


def decrement_like_on_model(*, instance, user: User):
    existing_bookmark = library.backend.get(instance=instance, user=user, key='like')
    existing_bookmark.delete()
    if hasattr(existing_bookmark, 'likes'):
        instance.likes -= 1
        instance.save()
