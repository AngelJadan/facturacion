# Generated by Django 3.2.12 on 2022-02-24 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(db_column='cli_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('nombreApellido', models.CharField(db_column='cli_nombre_apellido', default='sn', max_length=250, verbose_name='Nombre y Apellido')),
                ('identificacion', models.CharField(db_column='cli_identificacion', max_length=20, verbose_name='Identificacion')),
                ('tipoIdentificacion', models.CharField(choices=[('05', 'Cédula')], db_column='cli_tipo_identificacion', default='sn', max_length=5, verbose_name='Tipo de identificación')),
                ('direccion', models.CharField(db_column='cli_direccion', default='Sn', max_length=250, verbose_name='Dirección')),
                ('telefono', models.CharField(db_column='cli_telefono', default='Sn', max_length=20, verbose_name='Telefono')),
                ('extension', models.CharField(blank=True, db_column='cli_extension', default='sn', max_length=10, null=True, verbose_name='Extension')),
                ('movil', models.CharField(blank=True, db_column='cli_movil', default='sn', max_length=15, null=True, verbose_name='Movil')),
                ('mail', models.EmailField(db_column='cli_mail', default='sn', max_length=250, verbose_name='Mail')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Emisor',
            fields=[
                ('id', models.AutoField(db_column='emi_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('identificacion', models.CharField(db_column='emi_identificacion', max_length=20, unique=True, verbose_name='Identificacion')),
                ('tipo_id', models.CharField(choices=[('01', 'RUC'), ('05', 'Cedula')], db_column='emi_tipo_id', default='01', max_length=5, verbose_name='Tipo')),
                ('rasonSocial', models.CharField(db_column='emi_razon_social', default='sn', max_length=500, unique=True, verbose_name='Razón social')),
                ('nombreComercial', models.CharField(blank=True, db_column='emi_nombre_comercial', default='sn', max_length=255, null=True, unique=True, verbose_name='Nombre comercial')),
                ('telefono', models.CharField(blank=True, db_column='emi_telefono', default='sn', max_length=20, null=True, verbose_name='Telefono')),
                ('direccionMatriz', models.CharField(blank=True, db_column='emi_direccion_matriz', default='sn', max_length=255, null=True, verbose_name='Dirección matriz')),
                ('contribuyenteEspecial', models.CharField(blank=True, db_column='emi_contribuyente', default='sn', max_length=50, null=True, verbose_name='Contribuyente especial')),
                ('obligadoLlevarContabilidad', models.BooleanField(db_column='emi_obligado', default=False, verbose_name='Obligado')),
                ('regimenMicroempresa', models.BooleanField(db_column='emi_regimen_microempresa', default=False, verbose_name='Microempresa')),
                ('agenteRetencion', models.BooleanField(db_column='emi_agente_retencion', default=False, verbose_name='Agente de retención')),
                ('logo', models.CharField(blank=True, db_column='emi_logo', default='', max_length=250, null=True, verbose_name='Logo')),
                ('ambiente', models.CharField(choices=[('01', 'Pruebas'), ('02', 'Producción')], db_column='emi_ambiente', default='Prueba', max_length=2, verbose_name='Ambiente')),
                ('tipoToken', models.CharField(db_column='emi_tipo_token', default='', max_length=100, verbose_name='Tipo token')),
                ('firma', models.CharField(db_column='emi_firma', max_length=500, verbose_name='Firma')),
                ('estado', models.IntegerField(db_column='emi_estado', verbose_name='Estado')),
                ('cantidad_usuario', models.IntegerField(db_column='emi_cantidad_user', default=1, verbose_name='Cantidad de usuarios')),
                ('usuario', models.ForeignKey(db_column='emi_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Emisor',
                'verbose_name_plural': 'Emisores',
            },
        ),
        migrations.CreateModel(
            name='Establecimiento',
            fields=[
                ('id', models.AutoField(db_column='est_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('serie', models.CharField(db_column='est_serie', default='001', max_length=3, verbose_name='Serie')),
                ('nombre', models.CharField(blank=True, db_column='est_nombre', default='Sn', max_length=250, null=True, verbose_name='Nombre')),
                ('telefono', models.CharField(blank=True, db_column='est_telefono', default='Sn', max_length=250, null=True, verbose_name='Teléfono')),
                ('direccion', models.CharField(blank=True, db_column='est_direccion', default='Sn', max_length=250, null=True, verbose_name='Dirección')),
                ('emisor', models.ForeignKey(db_column='est_emisor', on_delete=django.db.models.deletion.CASCADE, to='ventas.emisor', verbose_name='Emisor')),
                ('usuario', models.ForeignKey(db_column='est_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Establecimiento',
                'verbose_name_plural': 'Establecimientos',
            },
        ),
        migrations.CreateModel(
            name='FacturaCabecera',
            fields=[
                ('id', models.AutoField(db_column='fac_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('secuencia', models.IntegerField(db_column='fac_secuencia', verbose_name='Secuencia')),
                ('autorizacion', models.CharField(db_column='fac_autorizacion', default='999', max_length=49, verbose_name='Autorizacion')),
                ('claveacceso', models.CharField(db_column='fac_claveacceso', default='999', max_length=49, verbose_name='Clave de acceso')),
                ('fecha', models.DateField(db_column='fac_fecha', verbose_name='Fecha')),
                ('establecimientoGuia', models.CharField(blank=True, db_column='fact_est_guia', default=None, max_length=3, null=True, verbose_name='Est. Guia')),
                ('puntoGuia', models.CharField(blank=True, db_column='fac_punto_guia', default=None, max_length=3, null=True, verbose_name='Punto de emisión')),
                ('secuenciaGuia', models.CharField(blank=True, db_column='fac_secuencia_guia', default=None, max_length=9, null=True, verbose_name='Secuencia de guia')),
                ('noobjetoiva', models.FloatField(db_column='fac_no_objetoiva', default=0.0, verbose_name='No objeto de IVA')),
                ('tarifa0', models.FloatField(db_column='fac_tarifa0', default=0.0, verbose_name='Tafira 0%')),
                ('tarifadif0', models.FloatField(db_column='fac_tarifadif0', default=0.0, verbose_name='Tafira diferente 0%')),
                ('excentoiva', models.FloatField(db_column='fac_excento', default=0.0, verbose_name='Excento IVA')),
                ('totaldescuento', models.FloatField(db_column='fac_total_descuento', default=0.0, verbose_name='Total descuento')),
                ('totalice', models.FloatField(db_column='fac_total_ice', default=0.0, verbose_name='Total ICE')),
                ('totalirbpnt', models.FloatField(db_column='fac_total_irbpnt', default=0.0, verbose_name='Total IRBPNT')),
                ('valorIva', models.FloatField(db_column='fac_valor_iva', default=0.0, verbose_name='Valor iva')),
                ('propina', models.FloatField(db_column='fac_propina', default=0, verbose_name='Propina')),
                ('total', models.FloatField(db_column='fac_total', default=0.0, verbose_name='Total')),
                ('estado', models.BooleanField(db_column='fac_estado', default=True, verbose_name='Estado')),
                ('cliente', models.ForeignKey(db_column='fac_cliente', on_delete=django.db.models.deletion.CASCADE, to='ventas.cliente', verbose_name='Cliente')),
                ('emisor', models.ForeignKey(db_column='fac_emisor', on_delete=django.db.models.deletion.CASCADE, to='ventas.emisor', verbose_name='Emisor')),
                ('establecimiento', models.ForeignKey(db_column='fac_establecimiento', on_delete=django.db.models.deletion.CASCADE, to='ventas.establecimiento', verbose_name='Establecimiento')),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
            },
        ),
        migrations.CreateModel(
            name='Iva',
            fields=[
                ('id', models.AutoField(db_column='iva_id', primary_key=True, serialize=False)),
                ('descripcion', models.CharField(blank=True, db_column='iva_descripcion', default='', max_length=250, null=True, verbose_name='Descripción')),
                ('porcentaje', models.FloatField(db_column='iva_porcentaje', default=0.0, unique=True, verbose_name='Porcentaje')),
                ('user', models.ForeignKey(db_column='iva_user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'IVA',
                'verbose_name_plural': 'IVAs',
            },
        ),
        migrations.CreateModel(
            name='NotaCredito',
            fields=[
                ('id', models.AutoField(db_column='ncr_id', primary_key=True, serialize=False)),
                ('secuencia', models.IntegerField(db_column='ncr_secuencia', verbose_name='Secuencia')),
                ('autorizacion', models.CharField(db_column='ncr_autorizacion', max_length=49, verbose_name='Autorización')),
                ('claveacceso', models.CharField(db_column='ncr_claveacceso', max_length=49, verbose_name='Clave de acceso')),
                ('fecha', models.DateField(db_column='ncr_fecha', verbose_name='Fecha')),
                ('comprobanteModificado', models.CharField(choices=[('01', 'Factura')], db_column='ncr_comp_mod', max_length=20, verbose_name='Comprobante modificado')),
                ('establecimientoDoc', models.CharField(db_column='ncr_comp_est_doc', max_length=3, verbose_name='Establecimiento comprobante')),
                ('puntoEmisionDoc', models.CharField(db_column='ncr_p_emi_doc', max_length=3, verbose_name='Punto de emisión comprobante')),
                ('secuenciaDoc', models.CharField(db_column='ncr_secuencia_doc', max_length=9, verbose_name='Secuencia comprobante')),
                ('motivo', models.CharField(blank=True, db_column='ncr_motivo', max_length=250, null=True, verbose_name='Motivo')),
                ('tarifa0', models.FloatField(db_column='ncr_tarifa0', default=0.0, verbose_name='Tarifa 0%')),
                ('tarifadif0', models.FloatField(db_column='ncr_tarifadif0', default=0.0, verbose_name='Tarifa diferente 0%')),
                ('noObjetoIva', models.FloatField(db_column='ncr_noobjetoiva', default=0.0, verbose_name='No objeto de IVA')),
                ('descuento', models.FloatField(db_column='ncr_descuento', default=0.0, verbose_name='Descuento')),
                ('excento', models.FloatField(db_column='ncr_excento', default=0.0, verbose_name='Excento')),
                ('valorIce', models.FloatField(db_column='ncr_valor_ice', default=0.0, verbose_name='Valor ICE')),
                ('valorirbpnr', models.FloatField(db_column='ncr_valor_ibpnr', default=0.0, verbose_name='Valor irbpnr')),
                ('iva', models.FloatField(db_column='ncr_iva', default=0.0, verbose_name='IVA')),
                ('total', models.FloatField(db_column='ncr_total', default=0.0, verbose_name='Total')),
                ('estado', models.CharField(choices=[('1', 'Emitido'), ('2', 'Anulado')], db_column='ncr_estado', default='1', max_length=5, verbose_name='Estado')),
                ('emisor', models.ForeignKey(db_column='ncr_emisor', on_delete=django.db.models.deletion.PROTECT, to='ventas.emisor', verbose_name='Emisor')),
                ('establecimiento', models.ForeignKey(db_column='ncr_est', on_delete=django.db.models.deletion.CASCADE, to='ventas.establecimiento', verbose_name='Establecimiento')),
            ],
            options={
                'verbose_name': 'Nota de crédito',
                'verbose_name_plural': 'Notas de crédito',
            },
        ),
        migrations.CreateModel(
            name='NotaDebito',
            fields=[
                ('id', models.AutoField(db_column='nde_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('secuencia', models.IntegerField(db_column='nde_secuencia', verbose_name='Secuencia')),
                ('autorizacion', models.CharField(db_column='nde_autorizacion', max_length=49, verbose_name='Autorización')),
                ('claveacceso', models.CharField(db_column='nde_claveacceso', max_length=49, verbose_name='Clave de acceso')),
                ('fecha', models.DateField(db_column='nde_fecha', verbose_name='Fecha')),
                ('comprobanteModificado', models.CharField(choices=[('01', 'Factura')], db_column='nde_comprobante', max_length=5, verbose_name='Comprobante')),
                ('establecimientoDoc', models.CharField(db_column='nde_comprobante_doc', default='001', max_length=3, verbose_name='Est. Comprobante')),
                ('puntoEmisionDoc', models.CharField(db_column='nde_p_emi_comprobante', default='001', max_length=3, verbose_name='Punto emisión comprobante')),
                ('secuenciaDoc', models.CharField(db_column='nde_secuencia_doc', default='000000001', max_length=9, verbose_name='Secuencia comprobante')),
                ('tarifa0', models.FloatField(db_column='nde_tarifa0', default=0.0, verbose_name='Tarifa 0%')),
                ('tarifadif0', models.FloatField(db_column='nde_tarifadif0', default=0.0, verbose_name='Tarifa diferente 0%')),
                ('noObjetoIva', models.FloatField(db_column='nde_no_objeto', default=0.0, verbose_name='No objeto IVA')),
                ('excento', models.FloatField(db_column='nde_excento', default=0.0, verbose_name='Excento')),
                ('valorIce', models.FloatField(db_column='nde_ice`', default=0.0, verbose_name='Valor ICE')),
                ('iva', models.FloatField(db_column='nde_iva', default=0.0, verbose_name='IVA')),
                ('total', models.FloatField(db_column='nde_total', default=0.0, verbose_name='Total')),
                ('estado', models.CharField(choices=[('1', 'Generado'), ('2', 'Anulado')], db_column='nde_estado', default='1', max_length=5, verbose_name='Estado')),
                ('cliente', models.ForeignKey(db_column='nde_cliente', on_delete=django.db.models.deletion.PROTECT, to='ventas.cliente', verbose_name='Cliente')),
                ('emisor', models.ForeignKey(db_column='nde_emisor', on_delete=django.db.models.deletion.CASCADE, to='ventas.emisor', verbose_name='Emisor')),
                ('establecimiento', models.ForeignKey(db_column='nde_est', on_delete=django.db.models.deletion.CASCADE, to='ventas.establecimiento', verbose_name='Establecimiento')),
            ],
            options={
                'verbose_name': 'Nota de Débito',
                'verbose_name_plural': 'Notas de Débito',
            },
        ),
        migrations.CreateModel(
            name='PuntoEmision',
            fields=[
                ('id', models.AutoField(db_column='pem_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('serie', models.CharField(db_column='pem_serie', default='001', max_length=3, verbose_name='Serie')),
                ('descripcion', models.CharField(db_column='pem_descripcion', default='sn', max_length=250, verbose_name='Descripción')),
                ('estado', models.BooleanField(db_column='pem_estado', default=False, verbose_name='Estado')),
                ('establecimiento', models.ForeignKey(db_column='pem_establecimiento', on_delete=django.db.models.deletion.PROTECT, related_name='puntos_emision', to='ventas.establecimiento', verbose_name='Establecimiento')),
                ('usuario', models.ForeignKey(db_column='pem_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Punto de emisión',
                'verbose_name_plural': 'Puntos de emisión',
            },
        ),
        migrations.CreateModel(
            name='Retencion',
            fields=[
                ('id', models.AutoField(db_column='ret_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('secuencia', models.CharField(db_column='ret_secuencia', max_length=9, verbose_name='Secuencia')),
                ('fecha', models.DateField(db_column='ret_fecha', verbose_name='Fecha')),
                ('tipo_documento', models.CharField(choices=[('01', '01:Factura')], db_column='ret_tipo_doc', max_length=50, verbose_name='Tipo de documento')),
                ('estab_doc', models.CharField(db_column='ret_estab_doc', max_length=3, verbose_name='Estab de documento')),
                ('pemis_doc', models.CharField(db_column='ret_pemis', max_length=3, verbose_name='Punto de emisión de documento')),
                ('secuencia_doc', models.CharField(db_column='ret_secuencia_doc', max_length=9, verbose_name='Secuencia documento')),
                ('autorizacion', models.CharField(db_column='ret_autorizacion', max_length=49, null=True, verbose_name='Autorización')),
                ('clave_acceso', models.CharField(db_column='ret_clave_acceso', max_length=49, verbose_name='Clave de acceso')),
                ('emisor', models.ForeignKey(db_column='ret_emisor', on_delete=django.db.models.deletion.PROTECT, to='ventas.emisor', verbose_name='Emisor')),
                ('establecimiento', models.ForeignKey(db_column='ret_establecimiento', on_delete=django.db.models.deletion.PROTECT, to='ventas.establecimiento', verbose_name='Establecimiento')),
                ('pemision', models.ForeignKey(db_column='ret_pemision', on_delete=django.db.models.deletion.PROTECT, to='ventas.puntoemision', verbose_name='Punto de emisión')),
                ('sujeto_retenido', models.ForeignKey(db_column='ret_sujeto', on_delete=django.db.models.deletion.PROTECT, to='ventas.cliente', verbose_name='Retenido')),
                ('usuario', models.ForeignKey(db_column='ret_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Retención',
                'verbose_name_plural': 'Retenciones',
            },
        ),
        migrations.CreateModel(
            name='RetencionCodigo',
            fields=[
                ('id', models.AutoField(db_column='rco_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('codigo', models.CharField(db_column='rco_codigo', max_length=20, verbose_name='Código')),
                ('porcentaje', models.FloatField(db_column='rco_porcentaje', verbose_name='Porcentaje')),
                ('detalle', models.CharField(db_column='rco_detalle', default='sn', max_length=255, verbose_name='Detalle')),
                ('tipo', models.CharField(db_column='rco_tipo', max_length=20, verbose_name='Tipo')),
                ('usuario', models.ForeignKey(db_column='rco_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Código de retención',
                'verbose_name_plural': 'Códigos de retenciones',
            },
        ),
        migrations.CreateModel(
            name='User_Emisor',
            fields=[
                ('id', models.AutoField(db_column='use_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('estado', models.BooleanField(db_column='use_estado', default=False, verbose_name='Estado')),
                ('emisor', models.ForeignKey(db_column='use_emisor', on_delete=django.db.models.deletion.PROTECT, to='ventas.emisor', verbose_name='Emisor')),
                ('user', models.ForeignKey(db_column='use_user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Usuario emisor',
                'verbose_name_plural': 'Usuarios emisor',
            },
        ),
        migrations.CreateModel(
            name='RetencionCompra',
            fields=[
                ('id', models.AutoField(db_column='rcp_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('baseImponible', models.FloatField(db_column='rcp_base_imp', default=0.0, verbose_name='Base imponible')),
                ('valor_retenido', models.FloatField(db_column='rcp_valor_retenido', default=0.0, verbose_name='Valor retenido')),
                ('emisor', models.ForeignKey(db_column='rcp_emisor', on_delete=django.db.models.deletion.PROTECT, to='ventas.emisor', verbose_name='Emisor')),
                ('retencion', models.ForeignKey(db_column='rcp_retencion', on_delete=django.db.models.deletion.PROTECT, to='ventas.retencion', verbose_name='Retención')),
                ('retencion_codigo', models.ForeignKey(db_column='rcp_retencion_codigo', on_delete=django.db.models.deletion.PROTECT, to='ventas.retencioncodigo', verbose_name='Código de retención')),
                ('usuario', models.ForeignKey(db_column='rcp_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Retención compra',
                'verbose_name_plural': 'Retenciones compras',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(db_column='pro_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('nombre', models.CharField(db_column='pro_nombre', max_length=250, verbose_name='Nombre')),
                ('codigoPrincipal', models.CharField(db_column='pro_principal', max_length=20, verbose_name='Código principal')),
                ('codigoAuxiliar', models.CharField(db_column='pro_auxiliar', max_length=20, verbose_name='Código auxiliar')),
                ('tipo', models.CharField(db_column='pro_tipo', max_length=20, verbose_name='Tipo')),
                ('ice', models.FloatField(db_column='pro_ice', verbose_name='ICE')),
                ('irbpnr', models.FloatField(db_column='pro_irbpnr', verbose_name='IRBPNR')),
                ('precio1', models.FloatField(db_column='pro_precio1', default=0.0, verbose_name='Precio 1')),
                ('precio2', models.FloatField(db_column='pro_precio2', default=0.0, verbose_name='Precio 2')),
                ('precio3', models.FloatField(db_column='pro_precio3', default=0.0, verbose_name='Precio 3')),
                ('precio4', models.FloatField(db_column='pro_precio4', default=0.0, verbose_name='Precio 4')),
                ('descripcion', models.CharField(blank=True, db_column='pro_descripcion', default='', max_length=255, verbose_name='Descripción')),
                ('emisor', models.ForeignKey(db_column='pro_emisor', on_delete=django.db.models.deletion.PROTECT, to='ventas.emisor', verbose_name='Emisor')),
                ('iva', models.ForeignKey(db_column='pro_iva', on_delete=django.db.models.deletion.PROTECT, to='ventas.iva', verbose_name='IVA')),
                ('usuario', models.ForeignKey(db_column='pro_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='OtroNDNC',
            fields=[
                ('id', models.AutoField(db_column='odc_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('nombre', models.CharField(db_column='odc_nombre', default='sn', max_length=255, verbose_name='Nombre')),
                ('descripcion', models.CharField(blank=True, db_column='odc_descripcion', default='', max_length=255, null=True, verbose_name='Descripcion')),
                ('notaCredito', models.ForeignKey(db_column='odc_nota_credit', on_delete=django.db.models.deletion.CASCADE, to='ventas.notacredito', verbose_name='Nota de crédito')),
                ('notaDebito', models.ForeignKey(db_column='odc_nota_debito', on_delete=django.db.models.deletion.CASCADE, to='ventas.notadebito', verbose_name='Nota de debito')),
                ('usuario', models.ForeignKey(db_column='odc_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Nota de crédito',
                'verbose_name_plural': 'Notas de crédito',
            },
        ),
        migrations.CreateModel(
            name='Otro',
            fields=[
                ('id', models.AutoField(db_column='otr_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('nombre', models.CharField(db_column='otr_nombre', max_length=250, verbose_name='Nombre')),
                ('descripcion', models.CharField(db_column='otr_descripcion', max_length=250, verbose_name='Descripción')),
                ('factura', models.ForeignKey(db_column='otr_factura', on_delete=django.db.models.deletion.CASCADE, to='ventas.facturacabecera', verbose_name='Factura')),
            ],
            options={
                'verbose_name': 'Otro',
                'verbose_name_plural': 'Otros',
            },
        ),
        migrations.AddField(
            model_name='notadebito',
            name='puntoEmision',
            field=models.ForeignKey(db_column='nde_p_emision', on_delete=django.db.models.deletion.CASCADE, to='ventas.puntoemision', verbose_name='Punto emisión'),
        ),
        migrations.AddField(
            model_name='notadebito',
            name='usuario',
            field=models.ForeignKey(db_column='nde_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AddField(
            model_name='notacredito',
            name='puntoEmision',
            field=models.ForeignKey(db_column='ncr_p_emision', on_delete=django.db.models.deletion.CASCADE, to='ventas.puntoemision', verbose_name='Punto de emisión'),
        ),
        migrations.AddField(
            model_name='notacredito',
            name='usuario',
            field=models.ForeignKey(db_column='ncr_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.CreateModel(
            name='FormaPago',
            fields=[
                ('id', models.AutoField(db_column='fpa_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('codigo', models.CharField(blank=True, db_column='fpa_codigo', default='', max_length=10, verbose_name='Código')),
                ('descripcion', models.CharField(blank=True, db_column='fpa_descripcion', default='', max_length=255, verbose_name='Descripción')),
                ('valor', models.FloatField(db_column='fpa_valor', default=0.0, verbose_name='Valor')),
                ('plazo', models.IntegerField(db_column='fpa_plazo', default=0.0, verbose_name='Plazo')),
                ('tiempo', models.IntegerField(db_column='fpa_tiempo', default=0.0, verbose_name='Tiempo')),
                ('factura', models.ForeignKey(db_column='fpa_factura', on_delete=django.db.models.deletion.PROTECT, to='ventas.facturacabecera', verbose_name='Factura')),
                ('notaDebito', models.ForeignKey(db_column='fpa_nota_debito', on_delete=django.db.models.deletion.PROTECT, to='ventas.notadebito', verbose_name='Nota debito')),
                ('usuario', models.ForeignKey(db_column='fpa_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Nota de débito',
                'verbose_name_plural': 'Notas de débito',
            },
        ),
        migrations.CreateModel(
            name='FacturaDetalle',
            fields=[
                ('id', models.AutoField(db_column='det_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('cantidad', models.FloatField(db_column='det_cantidad', default=0.0, verbose_name='Cantidad')),
                ('valorUnitario', models.FloatField(db_column='det_v_unitario', default=0.0, verbose_name='Valor unitario')),
                ('descuento', models.FloatField(db_column='det_descuento', default=0.0, verbose_name='Descuento')),
                ('ice', models.FloatField(db_column='det_ice', default=0.0, verbose_name='ICE')),
                ('valorTotal', models.FloatField(db_column='det_total', default=0.0, verbose_name='Total')),
                ('irbpnr', models.FloatField(db_column='det_irbpnr', default=0.0, verbose_name='IRBPNR')),
                ('factura', models.ForeignKey(db_column='det_factura', on_delete=django.db.models.deletion.CASCADE, to='ventas.facturacabecera', verbose_name='Factura cabecera')),
                ('producto', models.ForeignKey(db_column='det_producto', on_delete=django.db.models.deletion.CASCADE, to='ventas.producto', verbose_name='Producto')),
                ('usuario', models.ForeignKey(db_column='det_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Factura detalle',
                'verbose_name_plural': 'Facturas detalle',
            },
        ),
        migrations.AddField(
            model_name='facturacabecera',
            name='iva',
            field=models.ForeignKey(db_column='fac_iva', on_delete=django.db.models.deletion.CASCADE, to='ventas.iva', verbose_name='IVA'),
        ),
        migrations.AddField(
            model_name='facturacabecera',
            name='punto_emision',
            field=models.ForeignKey(db_column='fac_punto_emision', on_delete=django.db.models.deletion.CASCADE, to='ventas.puntoemision', verbose_name='Punto de emision'),
        ),
        migrations.AddField(
            model_name='facturacabecera',
            name='usuario',
            field=models.ForeignKey(db_column='fac_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.CreateModel(
            name='DetalleNC',
            fields=[
                ('id', models.AutoField(db_column='dnc_id', primary_key=True, serialize=False, verbose_name='Id')),
                ('cantidad', models.FloatField(db_column='dnc_cantidad', default=0.0, verbose_name='Cantidad')),
                ('valorUnitario', models.FloatField(db_column='dnc_valor_unitario', default=0.0, verbose_name='Valor Unitario')),
                ('descuento', models.FloatField(db_column='dnc_descuento', default=0.0, verbose_name='Descuento')),
                ('ice', models.FloatField(db_column='dnc_ice', default=0.0, verbose_name='ICE')),
                ('valorTotal', models.FloatField(db_column='dnc_valor_total', default=0.0, verbose_name='Valor total')),
                ('irbpnr', models.FloatField(db_column='dnc_irbpnr', default=0.0, verbose_name='IRBPNR')),
                ('notaCredito', models.ForeignKey(db_column='dnc_nota_credito', on_delete=django.db.models.deletion.CASCADE, to='ventas.notacredito', verbose_name='Nota de crédito')),
                ('producto', models.ForeignKey(db_column='dnc_producto', on_delete=django.db.models.deletion.CASCADE, to='ventas.producto', verbose_name='Producto')),
                ('usuario', models.ForeignKey(db_column='dnc_usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Detalle nota de crédito',
                'verbose_name_plural': 'Detalles Nota de crédito',
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='emisor',
            field=models.ForeignKey(db_column='cli_emisor', on_delete=django.db.models.deletion.PROTECT, to='ventas.emisor', verbose_name='Emisor'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuario',
            field=models.ForeignKey(db_column='cli_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
