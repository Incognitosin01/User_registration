# Generated by Django 3.2 on 2021-06-04 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='F_key',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]