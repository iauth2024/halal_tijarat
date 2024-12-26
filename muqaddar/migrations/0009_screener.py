# Generated by Django 5.1.3 on 2024-12-03 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muqaddar', '0008_performance_timeframe'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screener',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('clause', models.TextField(help_text='SQL-like clause for screener conditions')),
            ],
        ),
    ]
