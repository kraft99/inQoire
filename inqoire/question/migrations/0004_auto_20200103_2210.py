# Generated by Django 2.2.6 on 2020-01-04 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_remove_question_answered_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='asked_by_privacy',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Public (Everyone will see your profile next to question)'), (2, 'Anonymous (No one will see you posted this question)')], default=1, null=True),
        ),
    ]