# Generated by Django 2.2.6 on 2019-12-31 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comments_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]