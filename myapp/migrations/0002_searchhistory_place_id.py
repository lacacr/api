# Generated by Django 4.2.7 on 2023-11-25 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchhistory',
            name='place_id',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
