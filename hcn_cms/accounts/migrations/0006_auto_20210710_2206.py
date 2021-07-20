# Generated by Django 3.2.4 on 2021-07-10 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='reset_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='rest_token_expires',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]