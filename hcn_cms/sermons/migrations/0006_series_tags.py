# Generated by Django 3.2.4 on 2021-06-19 22:01

from django.db import migrations
import tagging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0005_auto_20210619_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='tags',
            field=tagging.fields.TagField(blank=True, max_length=255),
        ),
    ]
