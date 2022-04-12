from django.contrib import admin

from ventas.models import *

# Register your models here.

class EmisorAdmin(admin.ModelAdmin):
        list_display = (
                "id",
                "identificacion",
                "tipo_id",
                "rasonSocial",
                "nombreComercial",
                "telefono",
                "direccionMatriz",
                "contribuyenteEspecial",
                "obligadoLlevarContabilidad",
                "regimenMicroempresa",
                "agenteRetencion",
                "logo",
                "ambiente",
                "tipoToken",
                "firma",
                "estado",
                "cantidad_usuario",
                "usuario",
        )
        list_filter = ('ambiente','estado','cantidad_usuario','contribuyenteEspecial','obligadoLlevarContabilidad','regimenMicroempresa',
                       'agenteRetencion')
class User_EmisorAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'user',
            'estado',
            )
    
class EstablecimientoAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "serie",
            "nombre",
            "telefono",
            "direccion",
            "emisor",
            "usuario"
        )
    
class PuntoEmisionAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "serie",
            "descripcion",
            "establecimiento",
            "estado",
            "usuario"
        )
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "nombreApellido",
            "identificacion",
            "tipoIdentificacion",
            "direccion",
            "telefono",
            "extension",
            "movil",
            "mail",
            "usuario",
            "emisor"
        )
    
class IvaAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "descripcion",
            "porcentaje",
            "user"
        )
    

class ImpuestoAdmin(admin.ModelAdmin):
        list_display = (
                "id",
                "tipo",
                "codigo",
                "descripcion",
                "usuario"
        )

class ProductoAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "nombre",
            "codigoPrincipal",
            "codigoAuxiliar",
            "tipo",
            "precio1",
            "precio2",
            "precio3",
            "precio4",
            "descripcion",
            "emisor",
            "usuario"
        )

class ImpuestoProductoAdmin(admin.ModelAdmin):
        list_display = (
                "id",
                "impuesto",
                "producto",
                "usuario"
        )
    
class FacturaCabeceraAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "establecimiento",
            "punto_emision",
            "secuencia",
            "autorizacion",
            "claveacceso",
            "fecha",
            "emisor",
            "cliente",
            "establecimientoGuia",
            "puntoGuia",
            "secuenciaGuia",
            "propina",
            "estado",
            "usuario"
        )
    
   
class FacturaDetalleAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "cantidad",
            "valorUnitario",
            "descuento",
            "valorTotal",
            "factura",
            "producto",
            "usuario"
        )
    
class ImpuestoDetalleAdmin(admin.ModelAdmin):
        list_display = (
                "id",
                "codigoImpuesto",
                "tarifa",
                "baseImponible",
                "valor",
                "facturaDetalle"
        )
    
class NotaDebitoAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "establecimiento",
            "puntoEmision",
            "secuencia",
            "autorizacion",
            "claveacceso",
            "fecha",
            "comprobanteModificado",
            "establecimientoDoc",
            "puntoEmisionDoc",
            "secuenciaDoc",
            "tarifa0",
            "tarifadif0",
            "noObjetoIva",
            "excento",
            "valorIce",
            "iva",
            "total",
            "estado",
            "emisor",
            "cliente",
            "usuario",
        )
    
class OtroAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "nombre",
            "descripcion",
            "factura",
        )
    
class FormaPagoAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "codigo",
            "descripcion",
            "usuario",
        )

class FormaPagoFacturaAdmin(admin.ModelAdmin):
        list_display = (
                "id",
                "formaPago",
                "facturaid",
                "tiempo",
                "plazo",
                "valor",
                "usuario"
        )
        
class FormaPagoNotaDebitoAdmin(admin.ModelAdmin):
        list_display = (
                "id",
                "nota_debito",
                "forma_pago",
                "plazo",
                "valor",
                "usuario" 
        )
    

class NotaCreditoAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "establecimiento",
            "puntoEmision",
            "secuencia",
            "autorizacion",
            "claveacceso",
            "fecha",
            "comprobanteModificado",
            "establecimientoDoc",
            "puntoEmisionDoc",
            "secuenciaDoc",
            "motivo",
            "tarifa0",
            "tarifadif0",
            "noObjetoIva",
            "descuento",
            "excento",
            "valorIce",
            "valorirbpnr",
            "iva",
            "total",
            "estado",
            "emisor",
            "cliente",
            "usuario",
        )

class OtroNDNCAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "nombre",
            "descripcion",
            "notaDebito",
            "notaCredito",
            "usuario"
        )
    
class DetalleNCAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "cantidad",
            "valorUnitario",
            "descuento",
            "ice",
            "valorTotal",
            "irbpnr",
            "notaCredito",
            "producto",
            "usuario",
        )
    
class RetencionCodigoAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "codigo",
            "porcentaje",
            "detalle",
            "tipo",
            "usuario",
        )
    
class RetencionAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "emisor",
            "sujeto_retenido",
            "establecimiento",
            "pemision",
            "secuencia",
            "fecha",
            "tipo_documento",
            "estab_doc",
            "pemis_doc",
            "secuencia_doc",
            "autorizacion",
            "clave_acceso",
            "usuario",
        )
    
class RetencionCompraAdmin(admin.ModelAdmin):
    list_display = (
            "id",
            "baseImponible",
            "valor_retenido",
            "retencion",
            "retencion_codigo",
            "emisor",
            "usuario",
        )
    

admin.site.register(Emisor,EmisorAdmin)
admin.site.register(User_Emisor, User_EmisorAdmin)
admin.site.register(Establecimiento, EstablecimientoAdmin)
admin.site.register(PuntoEmision, PuntoEmisionAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Impuesto,ImpuestoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ImpuestoProducto, ImpuestoProductoAdmin)
admin.site.register(FacturaCabecera, FacturaCabeceraAdmin)
admin.site.register(FacturaDetalle, FacturaDetalleAdmin)
admin.site.register(ImpuestoDetalle,ImpuestoDetalleAdmin)
admin.site.register(NotaDebito, NotaDebitoAdmin)
admin.site.register(Otro, OtroAdmin)
admin.site.register(FormaPago, FormaPagoAdmin)
admin.site.register(FormaPagoFactura, FormaPagoFacturaAdmin)
admin.site.register(FormaPagoNotaDebito, FormaPagoNotaDebitoAdmin)
admin.site.register(NotaCredito, NotaCreditoAdmin)
admin.site.register(OtroNDNC, OtroNDNCAdmin)
admin.site.register(DetalleNC, DetalleNCAdmin)
admin.site.register(RetencionCodigo, RetencionCodigoAdmin)
admin.site.register(Retencion, RetencionAdmin)
admin.site.register(RetencionCompra, RetencionCompraAdmin)