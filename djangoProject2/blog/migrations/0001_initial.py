# Generated by Django 5.0.7 on 2024-08-03 13:46

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=250)),
                ('publish', models.DateTimeField(default=datetime.datetime(2024, 8, 3, 13, 46, 53, 812591, tzinfo=datetime.timezone.utc))),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PU', 'publish'), ('RE', 'Reject'), ('DR', 'Draft')], default='DF', max_length=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_Post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['publish'],
                'indexes': [models.Index(fields=['publish'], name='blog_post_publish_c4286e_idx')],
            },
        ),
    ]