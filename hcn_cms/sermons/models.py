from django.core.exceptions import ValidationError
from django.db import models
from djrichtextfield.models import RichTextField
from tagging.fields import TagField

# Create your models here.


def validate_sermon_notes(value):
    supported_types = ['application/pdf', 'application/msword', 'text/plain'
                       'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                       'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                       'application/vnd.ms-powerpoint']
    if value.file.content_type not in supported_types:
        raise ValidationError(u'Unsupported file type')


class Preacher(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='preacher', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True,)

    def __str__(self):
        return self.name


class Series(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(null=True)
    starts_at = models.DateField(null=True, db_index=True)
    ends_at = models.DateField(null=True, db_index=True)
    cover_image = models.ImageField(
        upload_to='series/%Y/%m/', null=True, blank=True)
    tags = TagField()

    class Meta:
        verbose_name_plural = 'Series'
        ordering = ['-starts_at']

    def __str__(self):
        return self.title


class Sermon(models.Model):
    """
    Model representing sermons. Link to sermin files (mp3 or mp4) is references from url.

    """
    title = models.CharField(max_length=255)
    preacher = models.ManyToManyField('Preacher', related_name='preacher', db_index=True)
    url = models.URLField(
        help_text="Link to sermon resource (recording or video) if any", null=True, blank=True)
    description = RichTextField(null=True)
    likes = models.PositiveIntegerField(default=0, null=True)
    published = models.DateTimeField(null=True, db_index=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    thumbnail = models.ImageField(
        upload_to='sermons/thumbs/%Y/%m/', null=True, blank=True)
    series = models.ForeignKey(
        'Series', on_delete=models.SET_NULL, null=True, db_index=True, related_name='sermons')
    sermon_notes = models.FileField(verbose_name='Sermon Notes', upload_to='static/sermon_notes/%Y/%m/',
                                    null=True, blank=True, validators=[validate_sermon_notes],
                                    help_text="upload only pdf, word, txt files")
    tags = TagField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at', '-published']

    @property
    def is_published(self) -> bool:
        return self.published is not None

    @property
    def who_is_preaching(self) -> str:
        return [value['name'] for value in self.preacher.values('name')]

    def is_liked_by_user(self, user_id: int) -> bool:
        if self.meta and 'liked_by' in self.meta:
            return user_id in self.meta['liked_by']

        return False

    def __str__(self):
        return self.title
