# Generated by Django 2.2.3 on 2020-08-23 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0011_auto_20200823_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consolidationgroup',
            name='source_of_funding',
        ),
    ]
