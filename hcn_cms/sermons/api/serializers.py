from rest_framework import serializers

from sermons.models import Series, Sermon


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Series
        fields = [
            'id',
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
        exclude = ['meta']
