# Generated by Django 2.2.3 on 2020-08-23 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0009_auto_20200823_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consolidationgroup',
            name='source_of_funding',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Funder'),
        ),
    ]
