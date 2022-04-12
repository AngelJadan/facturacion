# Generated by Django 3.2.12 on 2022-04-12 21:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ventas', '0027_remove_facturacabecera_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Impuesto',
            fields=[
                ('id', models.AutoField(db_column='imp_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('tipo', models.CharField(choices=[('2', 'IVA'), ('3', 'ICE'), ('5', 'IRBPNR')], db_column='imp_tipo', max_length=5, verbose_name='Tipo de impuesto')),
                ('codigo', models.CharField(db_column='imp_codigo', max_length=10, verbose_name='Código')),
                ('descripcion', models.CharField(blank=True, db_column='imp_descripcion', max_length=250, null=True, verbose_name='descripcion')),
                ('usuario', models.ForeignKey(db_column='imp_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Impuesto',
                'verbose_name_plural': 'Impuestos',
            },
        ),
        migrations.CreateModel(
            name='ImpuestoDetalle',
            fields=[
                ('id', models.AutoField(db_column='ide_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('codigoImpuesto', models.CharField(choices=[('2', 'IVA'), ('3', 'ICE'), ('5', 'IRBPNR')], db_column='ide_codigo_imp', max_length=5, verbose_name='Código de impuesto')),
                ('tarifa', models.FloatField(db_column='ide_tarifa', verbose_name='Tarifa')),
                ('baseImponible', models.FloatField(db_column='ide_base_imponible', verbose_name='Base imponible')),
                ('valor', models.FloatField(db_column='ide_valor', verbose_name='Valor impuesto')),
            ],
            options={
                'verbose_name': 'Impuesto detalle',
                'verbose_name_plural': 'Impuestos detalle',
            },
        ),
        migrations.CreateModel(
            name='ImpuestoProducto',
            fields=[
                ('id', models.AutoField(db_column='ipr_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('impuesto', models.ForeignKey(db_column='ipr_impuesto', on_delete=django.db.models.deletion.CASCADE, to='ventas.impuesto', verbose_name='Impuesto')),
            ],
            options={
                'verbose_name': 'Impuesto producto',
                'verbose_name_plural': 'Impuestos producto',
            },
        ),
        migrations.RemoveField(
            model_name='iva',
            name='user',
        ),
        migrations.RemoveField(
            model_name='facturadetalle',
            name='ice',
        ),
        migrations.RemoveField(
            model_name='facturadetalle',
            name='irbpnr',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='ice',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='irbpnr',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='tipo_iva',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='valor_iva',
        ),
        migrations.DeleteModel(
            name='ImpuestoFactura',
        ),
        migrations.DeleteModel(
            name='Iva',
        ),
        migrations.AddField(
            model_name='impuestoproducto',
            name='producto',
            field=models.ForeignKey(db_column='ipr_producto', on_delete=django.db.models.deletion.CASCADE, related_name='producto_impuestos', to='ventas.producto', verbose_name='Producto'),
        ),
        migrations.AddField(
            model_name='impuestoproducto',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='impuestodetalle',
            name='facturaDetalle',
            field=models.ForeignKey(db_column='ide_factura_detalle', on_delete=django.db.models.deletion.CASCADE, related_name='detalle_impuestos', to='ventas.facturadetalle', verbose_name='Factura detalle'),
        ),
    ]