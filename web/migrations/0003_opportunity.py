# Generated by Django 3.0.5 on 2020-04-25 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20200425_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Назва')),
                ('descr', models.TextField(verbose_name='Опис')),
                ('cost', models.IntegerField(default=0, verbose_name='Вартість')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='opportunities', to=settings.AUTH_USER_MODEL, verbose_name='Хто надає')),
            ],
            options={
                'verbose_name': 'Можливість',
                'verbose_name_plural': 'Можливості',
            },
        ),
    ]