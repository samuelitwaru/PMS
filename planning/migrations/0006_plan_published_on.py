# Generated by Django 2.2.3 on 2020-08-06 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0005_auto_20200805_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='published_on',
            field=models.DateField(null=True),
        ),
    ]
