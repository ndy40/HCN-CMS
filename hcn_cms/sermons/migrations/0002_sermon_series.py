# Generated by Django 3.2.4 on 2021-06-10 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sermons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sermon',
            name='series',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sermons.series'),
        ),
    ]
