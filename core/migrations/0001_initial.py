# Generated by Django 2.2.3 on 2020-08-04 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='SubProgramme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=128)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Programme')),
            ],
        ),
        migrations.CreateModel(
            name='Timing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.CharField(max_length=64)),
                ('start', models.DateField(null=True)),
                ('stop', models.DateField(null=True)),
                ('submission_deadline', models.DateField(null=True)),
                ('auto_submit', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserDepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('is_pdu', models.BooleanField(default=False)),
                ('budget_sealing', models.IntegerField(null=True)),
                ('hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sub_programme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.SubProgramme')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=128)),
                ('title', models.CharField(max_length=64)),
                ('telephone', models.CharField(max_length=16, unique=True)),
                ('is_ao', models.BooleanField(null=True)),
                ('is_in_pdu', models.BooleanField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.UserDepartment')),
            ],
        ),
        migrations.CreateModel(
            name='ConsolidationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_of_procurement', models.CharField(max_length=128, null=True)),
                ('contract_type', models.CharField(max_length=64, null=True)),
                ('prequalification', models.BooleanField(null=True)),
                ('bid_invitation_date', models.DateTimeField(null=True)),
                ('bid_opening_and_closing_date', models.DateTimeField(null=True)),
                ('approval_of_bid_evaluation_date', models.DateTimeField(null=True)),
                ('award_notification_date', models.DateTimeField(null=True)),
                ('contract_signing_date', models.DateTimeField(null=True)),
                ('contract_completion_date', models.DateTimeField(null=True)),
                ('expense', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Expense')),
            ],
        ),
    ]
