from django_filters.rest_framework import CharFilter, DjangoFilterBackend, FilterSet
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .serializers import SeriesSerializer, SermonsSerializer
from .services import increment_like_on_sermons
from sermons.models import Series, Sermon


# Create your views here.


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


class SermonDetail(RetrieveAPIView):
    queryset = Sermon.objects.all()
    serializer_class = SermonsSerializer


@api_view(['PATCH'])
def add_likes_to_sermons(request, pk):
    # todo:
    #  1. Validate the user and then increment the likes
    #  2. Make sure a user can only like a sermon once
    increment_like_on_sermons(sermon_id=pk)
    return Response(status=status.HTTP_204_NO_CONTENT)
