from importlib import import_module

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import CharFilter, DjangoFilterBackend, FilterSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response


from .serializers import SeriesSerializer, SermonsSerializer
from .services import bookmark_resource, decrement_like_on_model, increment_like_on_model
from bookmarking.exceptions import AlreadyExist, DoesNotExist
from bookmarking.handlers import library
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
@permission_classes([IsAuthenticated])
def update_likes_on_resource(request, pk, action, model: str):
    """
    Update likes on models.

    :param request:
    :param pk:
    :param action:
    :param model:
    :return:
    """
    try:
        module = import_module('sermons.models')
        klass = getattr(module, model.capitalize())
        instance = get_object_or_404(klass, pk=pk)

        if action == 'add_like':
            increment_like_on_model(instance=instance, user=request.user)
        elif action == 'remove_like':
            decrement_like_on_model(instance=instance, user=request.user)
        response = Response(status=status.HTTP_204_NO_CONTENT)
    except AlreadyExist:
        message = f'{model.capitalize()} #{instance.pk} is already bookmarked'
        response = Response(status=status.HTTP_400_BAD_REQUEST, data=message)
    except (ValueError, DoesNotExist) as e:
        message = f'{model.capitalize()} #{instance.pk} does not exists'
        response = Response(status=status.HTTP_400_BAD_REQUEST, data=message)

    return response


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_to_bookmark(request, pk, model):
    module = import_module('sermons.models')
    klass = getattr(module, model.capitalize())
    instance = get_object_or_404(klass, pk=pk)
    bookmark_resource(instance=instance, user=request.user)

    return Response(status=status.HTTP_204_NO_CONTENT, data='resource bookmarked')
