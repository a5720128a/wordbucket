# Generated by Django 2.0.1 on 2018-04-01 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordbucket', '0004_auto_20180401_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='date_pub',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
