# Generated by Django 4.0.4 on 2022-12-09 08:03

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cbtsystem', '0020_alter_testdate_next_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='testspec',
            name='studentResponseOne',
            field=jsonfield.fields.JSONField(default={}, null=True),
        ),
        migrations.AddField(
            model_name='testspec',
            name='studentResponseTwo',
            field=jsonfield.fields.JSONField(default={}, null=True),
        ),
    ]
