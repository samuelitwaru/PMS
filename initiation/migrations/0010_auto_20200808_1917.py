# Generated by Django 2.2.3 on 2020-08-08 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('initiation', '0009_auto_20200808_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='ao_approved_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='hod_approved_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='requisition',
            name='pdu_approved_on',
            field=models.DateField(null=True),
        ),
    ]
