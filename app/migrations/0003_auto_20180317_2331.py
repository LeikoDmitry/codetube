# Generated by Django 2.0.1 on 2018-03-17 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180317_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='image_filename',
        ),
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.ImageField(upload_to=''),
        ),
    ]
