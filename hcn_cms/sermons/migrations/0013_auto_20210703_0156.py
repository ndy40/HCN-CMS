# Generated by Django 3.2.4 on 2021-07-03 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0012_auto_20210703_0137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sermon',
            name='preacher',
        ),
        migrations.AddField(
            model_name='sermon',
            name='preacher',
            field=models.ManyToManyField(db_index=True, related_name='preacher', to='sermons.Preacher'),
        ),
    ]