# Generated by Django 2.1.3 on 2018-11-24 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20181118_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='classname',
            field=models.CharField(max_length=100),
        ),
    ]