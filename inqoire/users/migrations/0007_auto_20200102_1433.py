# Generated by Django 2.2.6 on 2020-01-02 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_register_ip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='register_ip',
            new_name='joined_with_ip',
        ),
    ]
