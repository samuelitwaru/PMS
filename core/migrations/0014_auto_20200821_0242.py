# Generated by Django 2.2.3 on 2020-08-21 02:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200821_0240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 21, 2, 42, 6, 209456, tzinfo=utc)),
        ),
    ]
