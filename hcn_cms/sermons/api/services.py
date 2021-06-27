from django.shortcuts import get_object_or_404

from sermons.models import Sermon


def increment_like_on_sermons(*, sermon_id: int):
    sermon = get_object_or_404(Sermon, pk=sermon_id)
    sermon.likes += 1
    sermon.save()
