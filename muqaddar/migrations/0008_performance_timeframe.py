# Generated by Django 5.1.3 on 2024-12-03 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muqaddar', '0007_performance'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='timeframe',
            field=models.CharField(default='N/A', max_length=255),
            preserve_default=False,
        ),
    ]