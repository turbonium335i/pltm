# Generated by Django 4.0.4 on 2023-02-07 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cbtsystem', '0024_accountprofile_showtest_alter_accountprofile_sex_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountprofile',
            old_name='showTest',
            new_name='allowed',
        ),
    ]
