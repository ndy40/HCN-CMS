from accounts.models import User
from bookmarking.exceptions import AlreadyExist, DoesNotExist
from bookmarking.handlers import library


def increment_like_on_model(*, instance, user: User):
    existing_bookmark = library.backend.filter(instance=instance, user=user)

    if existing_bookmark.exists():
        raise AlreadyExist(f'{type(instance)} {instance.id} already bookmarked')

    library.backend.add(user, instance, 'like')
    if hasattr(existing_bookmark, 'likes'):
        instance.likes += 1
        instance.save()
        return


def decrement_like_on_model(*, instance, user: User):
    existing_bookmark = library.backend.get(instance=instance, user=user, key='like')

    if not existing_bookmark:
        raise ValueError(message='bookmark not found')

    if hasattr(existing_bookmark, 'likes'):
        instance.likes -= 1
        instance.save()

    existing_bookmark.delete()


def bookmark_resource(*, instance, user: User):
    try:
        existing_bookmark = library.backend.get(instance=instance, user=user, key='bookmark')
        if existing_bookmark:
            raise AlreadyExist('resource already bookmarked')
    except DoesNotExist:
        library.backend.add(user, instance, 'bookmark')


def get_bookmarks_for_resource(user: User, model):
    return library.backend.filter(user=user, model=model, key='bookmark')


def has_user_bookmarked(user: User, pk, model, key='bookmark'):
    try:
        instance = model.objects.get(pk=pk)
        exists = library.backend.get(user=user, instance=instance, key=key)
        return exists is not None
    except DoesNotExist:
        return False
