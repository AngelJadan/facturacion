# Generated by Django 3.2.12 on 2022-03-28 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_auto_20220325_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='iva',
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo_iva',
            field=models.ForeignKey(db_column='pro_iva', default=1, on_delete=django.db.models.deletion.PROTECT, to='ventas.iva', verbose_name='Tipo IVA'),
        ),
        migrations.AddField(
            model_name='producto',
            name='valor_iva',
            field=models.FloatField(db_column='pro_valor_iva', default=0.0, verbose_name='Valor iva'),
        ),
    ]
