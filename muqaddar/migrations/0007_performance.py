# Generated by Django 5.1.3 on 2024-12-03 03:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muqaddar', '0006_stock_screener'),
    ]

    operations = [
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=20)),
                ('screener_name', models.CharField(max_length=100)),
                ('triggered_at', models.DateTimeField(default=datetime.datetime.now)),
                ('initial_price', models.FloatField()),
                ('current_price', models.FloatField(blank=True, null=True)),
                ('percent_change', models.FloatField(blank=True, null=True)),
                ('time_elapsed', models.DurationField(blank=True, null=True)),
            ],
        ),
    ]
