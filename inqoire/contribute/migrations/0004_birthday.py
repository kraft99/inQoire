# Generated by Django 2.2.6 on 2020-01-07 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribute', '0003_auto_20200104_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirthDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=125)),
                ('dob', models.DateTimeField()),
            ],
        ),
    ]
