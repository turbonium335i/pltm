# Generated by Django 4.0.4 on 2023-05-03 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cbtsystem', '0025_rename_showtest_accountprofile_allowed'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprofile',
            name='apifullname',
            field=models.CharField(blank=True, default='fullname', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='apiusername',
            field=models.CharField(blank=True, default='api username', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='accountprofile',
            name='age',
            field=models.PositiveIntegerField(blank=True, default=16, null=True),
        ),
    ]
