# Generated by Django 2.0.1 on 2018-04-01 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wordbucket', '0002_auto_20180401_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='pub_date',
        ),
    ]
