# Generated by Django 5.1.3 on 2024-12-23 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muqaddar', '0014_rename_alert_sent_at_performance_last_alert_sent_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='current_price',
        ),
    ]
