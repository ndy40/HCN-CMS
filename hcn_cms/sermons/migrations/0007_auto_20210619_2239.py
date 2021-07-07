# Generated by Django 3.2.4 on 2021-06-19 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0006_series_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/image/series/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='sermon',
            name='preacher',
            field=models.CharField(help_text='Name of preacher', max_length=225),
        ),
        migrations.AlterField(
            model_name='sermon',
            name='url',
            field=models.URLField(blank=True, help_text='Link to series resource if any', null=True),
        ),
    ]