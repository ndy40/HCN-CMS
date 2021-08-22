from django.shortcuts import get_object_or_404
from django_filters.rest_framework import CharFilter, DjangoFilterBackend, FilterSet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


from bookmarking.handlers import library
from bookmarking.exceptions import AlreadyExist, DoesNotExist

from .serializers import SeriesSerializer, SermonsSerializer
from .services import increment_like_on_sermons, decrement_like_on_sermon
from sermons.models import Series, Sermon


# Create your views here.

library.register([Sermon])


class SeriesLists(ListAPIView):
    class SeriesFilter(FilterSet):
        tags = CharFilter(field_name='tags', lookup_expr='icontains')
        title = CharFilter(field_name='title', lookup_expr='icontains')

        class Meta:
            model = Series
            fields = {
                'starts_at': ['lte', 'gte', ],
                'ends_at': ['lte', 'gte', ],
            }

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    filterset_class = SeriesFilter
    filter_backends = (DjangoFilterBackend,
                       OrderingFilter,)
    ordering_fields = ('starts_at', 'ends_at', 'title')


class SeriesDetail(RetrieveAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class SermonList(ListAPIView):
    class SermonsFilter(FilterSet):
        title = CharFilter(field_name='title', lookup_expr='icontains')
        tags = CharFilter(field_name='tags', lookup_expr='icontains')
        preacher = CharFilter(field_name='preacher', lookup_expr='icontains')
        series_name = CharFilter(field_name='series__name', lookup_expr='icontains')
        mime_type = CharFilter(field_name='mime_type', lookup_expr='exact')

        class Meta:
            model = Sermon
            fields = {
                'published': ['lte', 'gte'],
                'series': ['exact'],
            }

    queryset = Sermon.objects.all()
    serializer_class = SermonsSerializer
    filterset_class = SermonsFilter
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering_fields = ('published', 'created_at', 'updated_at', 'preacher', 'title', 'series')
    permission_classes = [IsAuthenticatedOrReadOnly]


class SermonDetail(RetrieveAPIView):
    queryset = Sermon.objects.all()
    serializer_class = SermonsSerializer


@api_view(['PATCH'])
def add_likes_to_sermons(request, pk):
    if request.user:
        try:
            sermon = get_object_or_404(Sermon, pk=pk)
            increment_like_on_sermons(sermon=sermon, user=request.user)
            response = Response(status=status.HTTP_204_NO_CONTENT)
        except AlreadyExist:
            response = Response(status=status.HTTP_204_NO_CONTENT)
        finally:
            return response

    raise PermissionDenied(detail='user must be authenticated for this operation')


@api_view(['PATCH'])
def remove_like_from_sermon(request, pk):
    if request.user:
        try:
            sermon = get_object_or_404(Sermon, pk=pk)
            decrement_like_on_sermon(sermon=sermon, user=request.user)
            response = Response(status=status.HTTP_204_NO_CONTENT)
        except DoesNotExist:
            response = Response(status=status.HTTP_400_BAD_REQUEST, data="Bookmark not found")
        finally:
            return response

    raise PermissionDenied(detail='user must be authenticated for this operation')
