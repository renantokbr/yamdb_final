# Generated by Django 2.2.16 on 2021-09-14 20:13

from django.db import migrations, models

import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20210913_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='review date'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[reviews.validators.year_validator], verbose_name='year'),
        ),
    ]
