# Generated by Django 2.2.3 on 2019-08-05 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190727_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('born', models.DateField()),
                ('died', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='movie',
            options={'ordering': ('-released', 'title')},
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Movie')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Person')),
            ],
            options={
                'unique_together': {('movie', 'person', 'name')},
            },
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, related_name='acting_credits', through='core.Role', to='core.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='directed', to='core.Person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(blank=True, related_name='writing_credits', to='core.Person'),
        ),
    ]