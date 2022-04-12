# Generated by Django 3.2.12 on 2022-04-12 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ventas', '0025_iva_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturacabecera',
            name='excentoiva',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='noobjetoiva',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='tarifa0',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='tarifadif0',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='tipo_iva',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='totaldescuento',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='totalice',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='totalirbpnt',
        ),
        migrations.RemoveField(
            model_name='facturacabecera',
            name='valor_iva',
        ),
        migrations.CreateModel(
            name='ImpuestoFactura',
            fields=[
                ('id', models.AutoField(db_column='ifa_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('base', models.FloatField(db_column='ifa_base', default=0, verbose_name='Base imponible')),
                ('valor', models.FloatField(db_column='ifa_valor', default=0, verbose_name='Valor impuesto')),
                ('facturaCabecera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='impuestos_factura', to='ventas.facturacabecera', verbose_name='Factura')),
                ('iva', models.ForeignKey(db_column='ifa_iva', on_delete=django.db.models.deletion.PROTECT, to='ventas.iva', verbose_name='Tipo de impuesto')),
                ('usuario', models.ForeignKey(db_column='ifa_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]