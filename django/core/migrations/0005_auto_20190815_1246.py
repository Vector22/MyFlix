# Generated by Django 2.2.3 on 2019-08-15 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190814_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='value',
            field=models.SmallIntegerField(choices=[(1, '👍'), (-1, '👎')], default=1),
        ),
    ]