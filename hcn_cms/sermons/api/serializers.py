from typing import OrderedDict
from rest_framework import serializers

from bookmarking.models import Bookmark

from sermons.models import Series, Sermon
from generic_relations.relations import GenericRelatedField


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Series
        fields = [
            '@id',
            'title',
            'description',
            'starts_at',
            'ends_at',
            'tags',
            'cover_image',
            'sermons']

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        ret['tags'] = ret['tags'].split(', ')

        return ret


class SermonsSerializer(serializers.HyperlinkedModelSerializer):
    preacher = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Sermon
        fields = '__all__'


class BookmarkedResourceSerializer(serializers.ModelSerializer):
    content_object = GenericRelatedField({
        Series: SeriesSerializer(),
        Sermon: SermonsSerializer(),
    })

    class Meta:
        model = Bookmark
        fields = ['content_object']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret['content_object']
