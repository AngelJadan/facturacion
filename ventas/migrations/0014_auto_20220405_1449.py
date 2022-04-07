# Generated by Django 3.2.12 on 2022-04-05 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ventas', '0013_auto_20220405_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otrondnc',
            name='notaCredito',
            field=models.ForeignKey(db_column='odc_nota_credit', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='odc_nota_credit', to='ventas.notacredito', verbose_name='Nota de crédito'),
        ),
        migrations.AlterField(
            model_name='otrondnc',
            name='notaDebito',
            field=models.ForeignKey(db_column='odc_nota_debito', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='odc_nota_debito', to='ventas.notadebito', verbose_name='Nota de debito'),
        ),
        migrations.AlterField(
            model_name='otrondnc',
            name='usuario',
            field=models.ForeignKey(db_column='odc_usuario', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]