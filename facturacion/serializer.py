from rest_framework import serializers
from ventas.models import *
from django.contrib.auth import password_validation, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator



def __validar_identificacion(identificacion = str, tipo=int):
    total = 0
    if tipo == 0: # cedula y r.u.c persona natural
        base = 10
        d_ver = int(identificacion[9])# digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1: # r.u.c. publicos
        base = 11
        d_ver = int(identificacion[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2 )
    elif tipo == 2: # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(identificacion[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0,len(multip)):
        p = int(identificacion[i]) * multip[i]
        if tipo == 0:
            total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])
        else:
            total+=p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver

def verificar(identificacion = str):
    l = len(identificacion)
    if l == 10 or l == 13: # verificar la longitud correcta
        cp = int(identificacion[0:2])
        if cp >= 1 and cp <= 22: # verificar codigo de provincia
            tercer_dig = int(identificacion[2])
            if tercer_dig >= 0 and tercer_dig < 6 : # numeros enter 0 y 6
                if l == 10:
                    return __validar_identificacion(identificacion,0)                       
                elif l == 13:
                    return __validar_identificacion(identificacion,0) and identificacion[10:13] != '000' # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_identificacion(identificacion,1) # sociedades publicas
            elif tercer_dig == 9: # si es ruc
                return __validar_identificacion(identificacion,2) # sociedades privadas
            else:
                raise Exception(u'Tercer digito invalido') 
        else:
            raise Exception(u'Codigo de provincia incorrecto') 
    else:
        raise Exception(u'Longitud incorrecta del numero ingresado')

class UserModelSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

class User_EmisorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User_Emisor
        fields = (
            'id',
            'user',
            'estado',
        )
        
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=User.objects.all())],
    )        
    username = serializers.CharField(
        min_length = 4,
        max_length = 20,
        validators = [UniqueValidator(queryset=User.objects.all())],
    )

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    
    def validation(self, data):
        user = authenticate(username=data['email'], password=data["password"])
        
        if not user:
            raise serializers.ValidationError("Las credenciales nos incorrectas.")
        
        
        self.context["user"] = user
        return data
    
    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context["user"])
        return self.context["user"], token.key

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class EmisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emisor
        
        def valid_tipo_identificacion(self):
            if self['tipo_id'] == '01':
                res = verificar(self['identificacion'])
                if res == False:
                    raise serializers.ValidationError('El número de RUC no es valido')
                
        #fields = '__all__'
        validators = [valid_tipo_identificacion]
        
        fields = (
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
        
class EstablecimientoSerializer(serializers.ModelSerializer):
    puntos_emision = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #puntos_emision = PuntoEmisionSerializer(many=True)
    class Meta:
        model = Establecimiento
        fields = (
            "id",
            "serie",
            "nombre",
            "telefono",
            "direccion",
            "emisor",
            "usuario",
            "puntos_emision"
        )

class PuntoEmisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PuntoEmision
        fields = (
            "id",
            "serie",
            "descripcion",
            "establecimiento",
            "estado",
            "usuario"
        )

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        
        def valid_documento(self):
            if self['tipoIdentificacion'] == "05":
                res = verificar(self['identificacion'])
                if res !=True:
                    raise serializers.ValidationError("El número de cedula no es valido")
            if self['tipoIdentificacion'] == "04":
                res = verificar(self['identificacion'])
                if res !=True:
                    raise serializers.ValidationError("El número de RUC no es valido")
        
        validators = [valid_documento]
        fields = (
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

class ImpuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Impuesto
        fields = (
            "id",
            "tipo",
            "codigo",
            "descripcion",
            "usuario"
        )
        
class ImpuestoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpuestoProducto
        fields = (
            "id",
            "impuesto",
            "producto",
            "usuario"
        )

class ProductoSerializer(serializers.ModelSerializer):
    producto_impuestos = ImpuestoProductoSerializer(many=True, read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'
    
    def create(self,validated_data):
        details_data =  validated_data.pop('producto_impuestos')
        producto = Producto.objects.create(**validated_data) # create the master reservation object
        for producto_impuesto in details_data:
            # create a details_reservation referencing the master reservation
            ImpuestoProducto.objects.create(**producto_impuesto, producto=producto)
        return producto

class OtroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otro
        fields = (
            "id",
            "nombre",
            "descripcion",
            "factura",
        )

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = (
            "id",
            "codigo",
            "descripcion",
            "usuario",
        )
        
class FormaPagoFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPagoFactura
        fields = (
            "id",
            "formaPago",
            "facturaid",
            "tiempo",
            "plazo",
            "valor",
            "usuario"
        )

class ImpuestoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImpuestoDetalle
        fields  = (
            "id",
            "codigoImpuesto",
            "tarifa",
            "baseImponible",
            "valor",
            "facturaDetalle"
        )


class FacturaDetalleSerializer(serializers.ModelSerializer):
    detalle_impuestos = ImpuestoDetalleSerializer(many=True, read_only=True)
    class Meta:
        model = FacturaDetalle
        fields = (
            "id",
            "cantidad",
            "valorUnitario",
            "descuento",
            "valorTotal",
            "factura",
            "producto",
            "usuario",
            "detalle_impuestos"
        )

class FacturaCabeceraSerializer(serializers.ModelSerializer):
    #factura_detalle = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #forma_pago_factura = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #otro_factura = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
        
    factura_detalle = FacturaDetalleSerializer(many=True, read_only=True)
    forma_pago_factura = FormaPagoFacturaSerializer(many=True, read_only=True)
    otro_factura = OtroSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = FacturaCabecera
        fields = (
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
            "usuario",
            "factura_detalle",
            "forma_pago_factura",
            "otro_factura"
        )
        
class FormaPagoNotaDebitoSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = FormaPagoNotaDebito
        fields = (
            "id",
            "nota_debito",
            "forma_pago",
            "plazo",
            "valor",
            "usuario"            
        )
        
class OtroNDNCSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtroNDNC
        fields = (
            "id",
            "nombre",
            "descripcion",
            "notaDebito",
            "notaCredito",
            "usuario"
        )

class NotaDebitoSerializer(serializers.ModelSerializer):
    forma_pago_debito = FormaPagoNotaDebitoSerializer(many=True, read_only=True)
    odc_nota_debito = OtroNDNCSerializer(many=True, read_only=True)
    class Meta:
        model = NotaDebito
        fields = (
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
            "forma_pago_debito",
            "odc_nota_debito"
        )

class DetalleNCSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleNC
        fields = (
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

class NotaCreditoSerializer(serializers.ModelSerializer):
    detalle_nota_credito = DetalleNCSerializer(many=True, read_only=True)
    odc_nota_credit = OtroNDNCSerializer(many=True, read_only=True)
    class Meta:
        model = NotaCredito
        fields = (
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
            "detalle_nota_credito",
            "odc_nota_credit"
        )

class RetencionCodigoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetencionCodigo
        fields = (
            "id",
            "codigo",
            "porcentaje",
            "detalle",
            "tipo",
            "usuario",
        )

class RetencionCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetencionCompra
        fields = (
            "id",
            "baseImponible",
            "valor_retenido",
            "retencion",
            "retencion_codigo",
            "emisor",
            "usuario"
        )

class RetencionSerializer(serializers.ModelSerializer):
    retenciones_compra = RetencionCompraSerializer(many=True, read_only=True)
    class Meta:
        model = Retencion
        fields = (
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
            "retenciones_compra"
        )


