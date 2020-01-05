# Generated by Django 2.2.6 on 2019-12-31 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('uuid_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.PositiveSmallIntegerField(choices=[(1, '<i class="la la-thumbs-up"></i>'), (-1, '<i class="la la-thumbs-down"></i>')])),
                ('object_id', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(limit_choices_to={'model__in': ('answer',)}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
                'unique_together': {('user', 'content_type', 'object_id')},
                'index_together': {('content_type', 'object_id')},
            },
        ),
    ]