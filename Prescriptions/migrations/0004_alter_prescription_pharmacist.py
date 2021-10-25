# Generated by Django 3.2.8 on 2021-10-24 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Prescriptions', '0003_alter_prescription_pharmacist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='pharmacist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pharmacist', to=settings.AUTH_USER_MODEL),
        ),
    ]
