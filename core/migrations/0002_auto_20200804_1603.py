# Generated by Django 2.2.3 on 2020-08-04 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consolidationgroup',
            old_name='approval_of_bid_evaluation_date',
            new_name='bid_evaluation_date',
        ),
    ]
