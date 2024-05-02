# Generated by Django 5.0.4 on 2024-05-02 07:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_description_alter_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 2, 7, 9, 12, 907926, tzinfo=datetime.timezone.utc)),
        ),
    ]