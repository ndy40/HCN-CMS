from django.shortcuts import get_object_or_404

from sermons.models import Sermon
from accounts.models import User

from bookmarking.handlers import library
from bookmarking.models import Bookmark
from bookmarking.exceptions import AlreadyExist


def increment_like_on_sermons(*, sermon: Sermon, user: User):
    existing_bookmark = library.backend.filter(instance=sermon, user=user)

    if not existing_bookmark.exists():
        library.backend.add(user, sermon, 'like')
        sermon.likes += 1
        sermon.save()

    raise AlreadyExist(f'Sermon {sermon.id} already bookmarked')


def decrement_like_on_sermon(*, sermon: Sermon, user: User):
    existing_bookmark = library.backend.get(instance=sermon, user=user, key='like')
    existing_bookmark.delete()
    sermon.likes -= 1
    sermon.save()

