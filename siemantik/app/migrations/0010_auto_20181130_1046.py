# Generated by Django 2.1.3 on 2018-11-30 10:46

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20181126_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classifiermodel',
            name='estimator',
            field=picklefield.fields.PickledObjectField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='classifiermodel',
            name='validation_results',
            field=picklefield.fields.PickledObjectField(editable=False, null=True),
        ),
    ]
