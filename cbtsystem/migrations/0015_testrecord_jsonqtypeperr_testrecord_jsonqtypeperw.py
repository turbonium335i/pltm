# Generated by Django 4.0.4 on 2022-05-29 14:05

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cbtsystem', '0014_qtypenote'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrecord',
            name='jsonQtypePerR',
            field=jsonfield.fields.JSONField(default={}, null=True),
        ),
        migrations.AddField(
            model_name='testrecord',
            name='jsonQtypePerW',
            field=jsonfield.fields.JSONField(default={}, null=True),
        ),
    ]
