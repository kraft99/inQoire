# Generated by Django 2.2.6 on 2020-01-02 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200102_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activated_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
