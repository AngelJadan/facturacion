from rest_framework import serializers
from ventas.models import *
from django.contrib.auth import password_validation, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

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
        #fields = '__all__'
        
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


class IvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iva
        fields = (
            "id",
            "descripcion",
            "porcentaje",
            "user"
        )


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = (
            "id",
            "nombre",
            "codigoPrincipal",
            "codigoAuxiliar",
            "tipo",
            "ice",
            "irbpnr",
            "precio1",
            "precio2",
            "precio3",
            "precio4",
            "iva",
            "descripcion",
            "emisor",
            "usuario"
        )


class FacturaCabeceraSerializer(serializers.ModelSerializer):
    facturaDetalle = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    otro = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    forma_pago = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
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
            "noobjetoiva",
            "tarifa0",
            "tarifadif0",
            "excentoiva",
            "totaldescuento",
            "totalice",
            "totalirbpnt",
            "iva",
            "valorIva",
            "propina",
            "total",
            "estado",
            "usuario",
            "facturaDetalle",
            "otro",
            "forma_pago_factura",
        )


class FacturaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaDetalle
        fields = (
            "id",
            "cantidad",
            "valorUnitario",
            "descuento",
            "ice",
            "valorTotal",
            "irbpnr",
            "factura",
            "producto",
            "usuario"
        )


class NotaDebitoSerializer(serializers.ModelSerializer):
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
        )


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


class NotaCreditoSerializer(serializers.ModelSerializer):
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
            "usuario",
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


class RetencionSerializer(serializers.ModelSerializer):
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
            "usuario",
        )
