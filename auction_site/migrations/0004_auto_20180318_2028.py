# Generated by Django 2.0.3 on 2018-03-18 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction_site', '0003_auto_20180318_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lot',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
