# Generated by Django 3.2.7 on 2021-09-30 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0018_auto_20210930_0244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sermon',
            name='mime_type',
        ),
        migrations.RemoveField(
            model_name='sermon',
            name='size',
        ),
    ]