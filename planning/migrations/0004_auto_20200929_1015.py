# Generated by Django 2.2.3 on 2020-09-29 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0003_auto_20200912_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='stage',
            field=models.CharField(default='PREPARATION', max_length=16, null=True),
        ),
    ]
