# Generated by Django 2.2.3 on 2020-08-25 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initiation', '0014_auto_20200809_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='source_of_funding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Funder'),
        ),
    ]
