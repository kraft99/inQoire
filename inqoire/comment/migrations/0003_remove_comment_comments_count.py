# Generated by Django 2.2.6 on 2019-12-31 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_comment_comments_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comments_count',
        ),
    ]