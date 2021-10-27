# Generated by Django 3.2.8 on 2021-10-26 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Prescriptions', '0005_auto_20211026_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicinequantity',
            name='medicine_cart',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Prescriptions.medicinecart'),
        ),
        migrations.AlterField(
            model_name='medicinequantity',
            name='prescription',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Prescriptions.prescription'),
        ),
    ]