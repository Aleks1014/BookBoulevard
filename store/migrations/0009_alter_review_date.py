# Generated by Django 5.0.4 on 2024-05-26 20:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 26, 20, 27, 4, 608807, tzinfo=datetime.timezone.utc)),
        ),
    ]
