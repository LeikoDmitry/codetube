# Generated by Django 2.0.1 on 2018-03-18 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('processed', models.BooleanField(default=False)),
                ('video_id', models.CharField(max_length=255, null=True)),
                ('video_filename', models.CharField(max_length=255, null=True)),
                ('visibility', models.CharField(choices=[(1, 'Public'), (2, 'Unlisted'), (3, 'Private')], max_length=255)),
                ('allow_votes', models.BooleanField(default=False)),
                ('allow_comment', models.BooleanField(default=True)),
                ('processed_percent', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Channel')),
            ],
        ),
    ]
