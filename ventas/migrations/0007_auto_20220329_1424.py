# Generated by Django 3.2.12 on 2022-03-29 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_auto_20220328_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facturacabecera',
            name='iva',
        ),
        migrations.AddField(
            model_name='facturacabecera',
            name='tipo_iva',
            field=models.ForeignKey(db_column='fac_iva', default=1, on_delete=django.db.models.deletion.CASCADE, to='ventas.iva', verbose_name='Tipo IVA'),
        ),
        migrations.AddField(
            model_name='facturacabecera',
            name='valor_iva',
            field=models.FloatField(db_column='fact_valor_iva', default=0.0, verbose_name='Valor iva'),
        ),
    ]