# Generated by Django 2.2.6 on 2020-01-02 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200102_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='register_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
