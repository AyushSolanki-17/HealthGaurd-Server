# Generated by Django 3.1.3 on 2020-12-30 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DiseasePrediction', '0002_auto_20201230_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testreport',
            name='desc',
        ),
        migrations.DeleteModel(
            name='TestReportDescription',
        ),
    ]
