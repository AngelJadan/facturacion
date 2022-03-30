# Generated by Django 3.2.12 on 2022-03-29 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0009_auto_20220329_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facturadetalle',
            name='factura',
            field=models.ForeignKey(db_column='det_factura', on_delete=django.db.models.deletion.PROTECT, related_name='factura_detalle', to='ventas.facturacabecera', verbose_name='Factura cabecera'),
        ),
    ]
