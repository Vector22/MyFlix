# Generated by Django 2.2.3 on 2019-08-15 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190815_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='value',
            field=models.SmallIntegerField(choices=[(1, '👍'), (-1, '👎')], null=True),
        ),
    ]
