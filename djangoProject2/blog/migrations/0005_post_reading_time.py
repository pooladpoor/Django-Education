# Generated by Django 5.1 on 2024-08-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reading_time',
            field=models.PositiveIntegerField(default=0, verbose_name='زمان مطالعه'),
            preserve_default=False,
        ),
    ]