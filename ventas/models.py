from django.db import models
from django.contrib.auth.models import User
from numpy import choose

# Create your models here.

class Emisor(models.Model):
    TYPE_ID = (
        ("1","Cedula"),
    )
    _id = models.AutoField(db_column='emi_id', primary_key=True, verbose_name="Id")
    _identificacion = models.CharField(db_column="emi_identificacion", unique=True, max_length="20", null=False, blank=False, verbose_name="Identificacion", default="sn")
    _tipo_id = models.CharfField(db_column="emi_tipo_id", null=False, blank=False, max_length="20", choices=TYPE_ID, default="01", verbose_name="Tipo")
    _rasonSocial = models.CharField(db_column="emi_razon_social", max_length="500", null=False, blank=False, unique=True, default="sn", verbose_name="Razón social")
    _nombreComercial = models.CharField(db_column="emi_nombre_comercial", max_length="20", null=True, blank=True, unique=True, default="sn", verbose_name="Nombre comercial")
    _telefono = models.CharField(db_column="emi_telefono", max_length="20", null=True, blank=True, default="sn", verbose_name="Telefono")
    _direccionMatriz = models.CharField(db_column="emi_direccion_matriz", max_length="20", null=True, blank=True, default="sn", verbose_name="Dirección matriz")
    _contribuyenteEspecial = models.CharField(db_column="emi_contribuyente", max_length="50", null=True, blank=True, default="sn", verbose_name="Contribuyente especial")
    _obligadoLlevarContabilidad = models.BooleanField(db_column="emi_obligado", null=False, blank=False, default=False, verbose_name="Obligado")
    _regimenMicroempresa = models.BooleanField(db_column="emi_regimen_microempresa", null=False, blank=False, default=False, verbose_name="Microempresa")
    _agenteRetencion = models.BooleanField(db_column="emi_agente_retencion", null=False, blank=False, default=False, verbose_name="Agente de retención")
    _logo = models.CharField(db_column="emi_logo", max_length="250", null=False, blank=False, default=False, verbose_name="Logo")
    _ambiente = models.IntegerField(db_column="emi_ambiente", null=False, blank=False, default=False, verbose_name="Ambiente")
    _tipoToken = models.CharField(db_column="emi_tipo_token", null=False, blank=False, default=False, verbose_name="Tipo token")
    _firma = models.CharField(db_column="emi_firma", null=False, blank=False, verbose_name="Firma")
    _estado = models.IntegerField(db_column="emi_estado", null=False, blank = False, verbose_name="Estado")
    _usuario = models.ForeignKey(User, db_column="emi_usuario", on_delete=models.CASCADE, null=False, blank = False, verbose_name="Usuario")

    def __str__(self):
        return str(self._id)

    class Meta:
        verbose_name = "Emisor"
        verbose_name_plural = "Emisores"
    
    def validarIdentificacion(_identificacion):
        try:
            l = len(_identificacion)
            if l == 10 or l == 13: # verificar la longitud correcta
                cp = int(_identificacion[0:2])
                if cp >= 1 and cp <= 22: # verificar codigo de provincia
                    tercer_dig = int(_identificacion[2])
                    if tercer_dig >= 0 and tercer_dig < 6 : # numeros enter 0 y 6
                        if l == 10:
                            return __validar_ced_ruc(_identificacion,0)                       
                        elif l == 13:
                            return __validar_ced_ruc(_identificacion,0) and _identificacion[10:13] != '000' # se verifica q los ultimos numeros no sean 000
                    elif tercer_dig == 6:
                        return __validar_ced_ruc(_identificacion,1) # sociedades publicas
                    elif tercer_dig == 9: # si es ruc
                        return __validar_ced_ruc(_identificacion,2) # sociedades privadas
                    else:
                        raise Exception(u'Tercer digito invalido') 
                else:
                    raise Exception(u'Codigo de provincia incorrecto') 
            else:
                raise Exception(u'Longitud incorrecta del numero ingresado')
        except BaseException as ex:
            return ex

    def __validar_ced_ruc(nro,tipo):
        total = 0
        if tipo == 0: # cedula y r.u.c persona natural
            base = 10
            d_ver = int(nro[9])# digito verificador
            multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
        elif tipo == 1: # r.u.c. publicos
            base = 11
            d_ver = int(nro[8])
            multip = (3, 2, 7, 6, 5, 4, 3, 2 )
        elif tipo == 2: # r.u.c. juridicos y extranjeros sin cedula
            base = 11
            d_ver = int(nro[9])
            multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
        for i in range(0,len(multip)):
            p = int(nro[i]) * multip[i]
            if tipo == 0:
                total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])
            else:
                total+=p
        mod = total % base
        val = base - mod if mod != 0 else 0
        return val == d_ver

    def crearEmisor(emisor):
        try:
            emisor.save()
            return emisor
        except BaseException as ex:
            return ex
    
    def buscarEmisor(identificacion = str):
        try:
            return Emisor.objects.get(_identificacion=identificacion)
        except BaseException as ex:
            return ex
    
    def buscarEmisor_id(id=int):
        try:
            return Emisor.objects.get(_id=id)
        except BaseException as ex:
            return ex
    
    def actualizarEmisor(emisor):
        try:
            Emisor.objects.filter(_id=emisor.id).update(_identificacion=emisor.identificacion, _tipo_id=emisor.tipo_id\
            ,_rasonSocial = emisor._rasonSocial, _nombreComercial = emisor._nombreComercial, _telefono = emisor._telefono\
            ,_direccionMatriz = emisor._direccionMatriz, _contribuyenteEspecial = emisor._contribuyenteEspecial, _obligadoLlevarContabilidad= emisor._obligadoLlevarContabilidad\
            ,_regimenMicroempresa = emisor._regimenMicroempresa, _agenteRetencion = emisor._agenteRetencion, _logo = emisor._logo\
            ,_ambiente=emisor._ambiente, _tipoToken = emisor._tipoToken, _firma = emisor._firma, _estado = emisor._estado\
            ,_usuario=emisor._usuario)
            return True
        except BaseException as ex:
            return ex
    


class User_Emisor(models.Model):
    _id = models.AutoField(db_column='use_id', primary_key=True, verbose_name="Id")
    _user = models.ForeignKey(User, db_column="use_user", on_delete=models.CASCADE, verbose_name="Usuario")
    _estado = models.BooleanField(db_column="use_estado", default=False, verbose_name="Estado")

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = "Usuario emisor"
        verbose_name_plural = "Usuarios emisor"
    
    def create(user_emisor):
        try:
            user_emisor.save()
            return user_emisor.id
        except BaseException as ex:
            return ex
    def search(id):
        try:
            return User_Emisor.objects.get(id=id)
        except BaseException as ex:
            return ex


class Establecimiento(models.Model):
    _id = models.AutoField(db_column="est_id", primary_key=True, verbose_name="Id")
    _serie = models.CharField(db_column="est_serie", max_length="3", null=False, blank=False, default="001", verbose_name="Serie")
    _nombre = models.CharField(db_column="est_nombre", max_length="250", null=True, blank=True, default="Sn", verbose_name="Nombre")
    _telefono = models.CharField(db_column="est_telefono", max_length="250", null=True, blank=True, default="Sn", verbose_name="Teléfono")
    _direccion = models.CharField(db_column="est_direccion", max_length="250", null=True, blank=True, default="Sn", verbose_name="Dirección")
    _emisor = models.ForeignKey(Emisor, db_column="est_emisor", on_delete=models.CASCADE, verbose_name="Establecimiento")
    _usuario = models.ForeignKey(User, on_delete=models.CASCADE,db_column="est_usuario", verbose_name="Usuario")

    class Meta:
        verbose_name = "Establecimiento"
        verbose_name_plural = "Establecimientos"
    
    def __str__(self):
        return str(self._id)
    
    def create(establecimiento):
        try:
            establecimiento.save()
            return establecimiento
        except BaseException as ex:
            return ex
    
    def search_id(id):
        try:
            return Establecimiento.objects.get(_id=id)
        except BaseException as ex:
            return ex
        
    def delete(id):
        try:
            Establecimiento.objects.filter(_id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_emisor(emisor_id = int):
        try:
            return Emisor.objects.filter(_id=emisor_id)
        except BaseException as ex:
            return ex


class PuntoEmision(models.Model):
    _id = models.AutoField(db_column="pem_id", primary_key=True, verbose_name="Id")
    _serie = models.CharField(db_column="pem_serie", max_length=3, null=False, blank=False, default="001", verbose_name="Serie")
    _descripcion = models.CharField(db_column="pem_descripcion", max_length='250', null=False, blank=False, default="sn", verbose_name="Descripción")
    _establecimiento = models.ForeignKey(Establecimiento, db_column="pem_establecimiento", verbose_name="Establecimiento")
    _estado = models.BooleanField(db_column="pem_estado", null=False, blank=False, default=False, verbose_name="Estado")
    _usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column="pem_usuario", verbose_name="Usuario")

    def __str__(self):
        return str(self._id)
        

    class Meta:
        verbose_name = "Punto de emisión"
        verbose_name_plural = "Puntos de emisión"

    def create(puntoEmision):
        try:
            puntoEmision.save()
            return puntoEmision
        except BaseException as ex:
            return ex

    def search_id(id = int):
        try:
            return PuntoEmision.objects.get(id=id)
        except BaseException as ex:
            return ex
        
    def delete(id = int):
        try:
            PuntoEmision.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex
    def list_to_establecimiento(establecimiento_id=int):
        try:
            return PuntoEmision.objects.filter(establecimiento_id=establecimiento_id)
        except BaseException as ex:
            return ex
        
class Cliente(models.Model):
    TYPE_ID=(
        ("05","Cédula"),)
    
    _id = models.AutoField(db_column="cli_id", primary_key=True, verbose_name="Id")
    _nombreApellido = models.CharField(db_column="cli_nombre_apellido", max_length=250, null=False, blank=False, verbose_name="Nombre y Apellido")
    _identificacion = models.CharField(db_column="cli_identificacion", max_length=20, null=False, blank=False, verbose_name="Identificacion")
    _tipoIdentificacion = models.CharField(db_column="cli_tipo_identificacion", max_length=20, null=False, blank=False, choose = TYPE_ID, verbose="Tipo de identificación")
    _direccion = models.CharField(db_column="cli_direccion", max_length=250, null=False, blank=False, default="Sn", verbose_name="Dirección")
    _telefono = models.CharField(db_column="cli_telefono", max_length=20, null=False, blank = False, default = "Sn", verbose_name="Telefono")
    _extension = models.CharField(db_column="cli_extension", max_length=10, null=True, blank=True, default=None, verbose_name="Extension")
    _movil = models.CharField(db_column="cli_movil", max_length=15, null=True, blank=True, default="", verbose_name="Movil")
    _mail = models.EmailField(db_column="cli_mail", max_length=250, null=False, blank=False, verbose_name="Mail")
    _usuario = models.ForeignKey(User, db_column="cli_usuario", on_delete=models.CASCADE, verbose_name="Usuario")
    _emisor = models.ForeignKey(Emisor, db_column="cli_emisor", on_delete=models.CASCADE, verbose_name="Emisor")
    
    def __str__(self):
        return str(self._id)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    
    def create(cliente):
        try:
            cliente.save()
            return cliente._id
        except BaseException as ex:
            return ex
        
    def search(id):
        try:
            return Cliente.objects.get(id=id)
        except BaseException as ex:
            return ex
        
    def delete(id):
        try:
            Cliente.objects.delete(id=id)
            return True
        except BaseException as ex:
            return ex
    
    def list(emisor_id = int):
        try:
            return Cliente.objects.list(emisor_id=emisor_id)
        except BaseException as ex:
            return ex
        


class Iva(models.Model):
    _id = models.AutoField(db_column="iva_id", primary_key=True)
    _descripcion = models.CharField(db_column="iva_descripcion", max_length=250, null=True, blank=True, verbose_name='Descripción')
    _porcentaje = models.FloatField(db_column="iva_porcentaje", null=False, blank=False, default=0.00, verbose_name='Porcentaje')
    _user = models.ForeignKey(User, db_column="iva_user", on_delete=models.CASCADE, verbose_name="Usuario")
    
    def __str__(self):
        return str(self._id)

    class Meta:
        verbose_name = "IVA"
        verbose_name_plural = "IVAs"
        
    def create(iva):
        try:
            iva.save()
            return iva._id
        except BaseException as ex:
            return ex
    
    def search(id = int):
        try:
            return Iva.objects.get(id=id)
        except BaseException as ex:
            return ex
    
    def remove(id = int):
        try:
            Iva.objects.delete(id=id)
            return True
        except BaseException as ex:
            return ex
        
    def list():
        try:
            return Iva.objects.all().order_by("porcentaje")
        except BaseException as ex:
            return ex

class Producto(models.Model):
    _id = models.AutoField(db_column='pro_id', primary_key=True, verbose_name="Id")
    _nombre = models.CharField(db_column='pro_nombre', maxlength=250, null=False, blank=False, verbose_name="Nombre")
    _codigoPrincipal = models.CharfField(db_column='pro_principal', maxlength=20, null=False, blank=False, verbose_name="Código principal")
    _codigoAuxiliar = models.CharfField(db_column='pro_auxiliar', maxlength=20, null=False, blank=False, verbose_name="Código auxiliar")
    _tipo = models.CharfField(db_column='pro_tipo', maxlength=20, null=False, blank=False, verbose_name="Tipo")
    _ice = models.FloatField(db_column="pro_ice", null=False, blank=False, verbose_name="ICE")
    _irbpnr = models.FloatField(db_column="pro_irbpnr", null=False, blank=False, verbose_name="IRBPNR")
    _precio1 = models.FloatField(db_column="pro_precio1", null=False, blank=False, default = 0.00, verbose_name="Precio 1")
    _precio2 = models.FloatField(db_column="pro_precio2", null=False, blank=False, default = 0.00, verbose_name="Precio 2")
    _precio3 = models.FloatField(db_column="pro_precio3", null=False, blank=False, default = 0.00, verbose_name="Precio 3")
    _precio4 = models.FloatField(db_column="pro_precio4", null=False, blank=False, default = 0.00, verbose_name="Precio 4")
    _iva = models.ForeignKey(Iva, db_column="pro_iva", on_delete=models.PROTECT, verbose_name="IVA")
    _descripcion = models.CharField(db_column="pro_descripcion", null=False, blank=True, default="", verbose_name="Descripción")
    _emisor = models.ForeignKey(Emisor, db_column="pro_emisor", on_delete=models.PROTECT, verbose_name="Emisor")
    _usuario = models.ForeignKey(User, db_column="pro_usuario", on_delete=models.CASCADE, verbose_name="Usuario")
    
    def __str__(self):
        return str(self._id)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def create(producto):
        try:
            producto.save()
            return producto._id
        except BaseException as ex:
            return ex
        
    def search(id=int):
        try:
            return Producto.objects.get(_id=id)
        except BaseException as ex:
            return ex
        
    def update(producto):
        try:
            Producto.objects.filter(_id=producto.id).update(_nombre=producto.nombre\
            ,_codigoPrincipal = producto._codigoPrincipal, _codigoAuxiliar=producto._codigoAuxiliar\
            ,_tipo = producto._tipo, _ice=producto._ice, _irbpnr= producto._irbpnr\
            ,_precio1=producto._precio1,_precio2 = producto._precio2, _precio3=producto._precio3\
            ,_precio4 = producto._precio4,_iva= producto._iva,_descripcion=producto._descripcion\
            ,_emisor = producto._emisor,_usuario=producto._usuario)
            return True
        except BaseException as e:
            return e
    
    def remove(id = int):
        try:
            Producto.objects.filter(_id=id).delete()
            return True
        except BaseException as ex:
            return ex
        
    def list_to_emisor(id_emisor = int):
        try:
            return Producto.objects.filter(_emisor=id_emisor)
        except BaseException as ex:
            return ex
        

class FacturaCabecera(models.Model):
    _id = models.AutoField(db_column="fac_id", primary_key=True, verbose_name="Id")
    _establecimiento = models.ForeignKey(Establecimiento, db_column="fac_establecimiento", on_delete=models.CASCADE, verbose_name="Establecimiento")
    _punto_emision = models.ForeignKey(PuntoEmision, db_column="fac_punto_emision", on_delete=models.CASCADE, verbose_name="Punto de emision")
    _secuencia = models.IntegerField(db_column="fac_secuencia", null=False, blank=False, verbose_name="Secuencia")
    _autorizacion = models.CharField(db_column="fac_autorizacion", max_length="49", null=False, blank=False, verbose_name="Autorizacion", default="999", verbose_name="Autorización")
    _claveacceso = models.CharField(db_column="fac_claveacceso", max_length="49", null=False, blank=False, verbose_name="Clave de acceso", default="999", verbose_name="Clave de acceso")
    _fecha = models.DateField(db_column="fac_fecha", null=False, blank=False, verbose_name="Fecha")
    _emisor = models.ForeignKey(Emisor, db_column="fac_emisor", on_delete=models.CASCADE, verbose_name="Emisor")
    _cliente = models.ForeignKey(Cliente, db_column="fac_cliente", on_delete=models.CASCADE, verbose_name="Cliente")
    _establecimientoGuia = models.CharField(db_column="fact_est_guia", max_length="3", null=True, blank=True, default=None, verbose = "Est. Guia")
    _puntoGuia = models.CharField(db_column="fac_punto_guia", max_length="3", null=True, blank=True, default=None, verbose = "Punto de emisión")
    _secuenciaGuia = models.CharField(db_column="fac_secuencia", max_length="9", null=True, blank=True, default=None, verbose = "Secuencia de guia")
    _noobjetoiva = models.FloatField(db_column="fac_no_objetoiva", null=False, blank=False, default=0.00, verbose = "No objeto de IVA")
    _tarifa0 = models.FloatField(db_column="fac_tarifa0", null=False, blank=False, default=0.00, verbose = "Tafira 0%")
    _tarifadif0 = models.FloatField(db_column="fac_tarifadif0", null=False, blank=False, default=0.00, verbose = "Tafira diferente 0%")
    _excentoiva = models.FloatField(db_column="fac_excento", null=False, blank=False, default=0.00, verbose = "Excento IVA")
    _totaldescuento = models.FloatField(db_column="fac_total_descuento", null=False, blank=False, default=0.00, verbose = "Total descuento")
    _totalice = models.FloatField(db_column="fac_total_ice", null=False, blank=False, default=0.00, verbose = "Total ICE")
    _totalirbpnt = models.FloatField(db_column="fac_total_irbpnt", null=False, blank=False, default=0.00, verbose = "Total IRBPNT")
    _iva = models.ForeignKey(Iva, db_column="fac_iva", on_delete=models.CASCADE, verbose = "IVA")
    _valorIva = models.FloatField(db_column="fac_valor_iva", null=False, blank=False, default=0.00, verbose="Valor iva")
    _propina = models.FloatField(db_column="fac_propina", null=False, blank=False, default=0, verbose_name="Propina")
    _total = models.FloatField(db_column="fac_total", null=False, blank=False, default=0.00, verbose_name="Total")
    _estado = models.BooleanField(db_column="fac_estado", null=False, blank=False, default=True, verbose_name="Estado")
    _usuario = models.ForeignKey(User, db_column="fac_usuario", null=False, blank=False, verbose_name="Usuario")
    
    def __str__(self):
        return str(self._id)
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        
    def create(factura):
        try:
            factura.save()
            return factura.id
        except BaseException as ex:
            return ex
        
    def search_to_id(id = int):
        try:
            return FacturaCabecera.objects.get(_id=id)
        except BaseException as ex:
            return ex
        
    def search_to_factura(establecimiento = str, punto_emision=str, secuencia=str, emisor_id = int):
        est = None
        p_emi = None
        emis = None
        
        try:
            est = Establecimiento.objects.get(_serie = establecimiento)
            p_emi = PuntoEmision.objects.get(_serie = punto_emision)
            emis = Emisor.objects.get(id=emisor_id)
            
            if est!=None and p_emi!=None and emis!=None:
                return FacturaCabecera.objects.filter(_establecimiento=est, _punto_emision=p_emi, _secuencia=secuencia, _emisor = emis)
            else:
                return []
            
        except BaseException as ex:
            return ex

    def remove(id = int):
        try:
            FacturaCabecera.objects.filter(_id=id)
            return True
        except BaseException as ex:
            return ex
    
    def list_to_mont_year(month=str, year=str, emisor_id = int):
        try:
            emis = Emisor.objects.get(_id=emisor_id)
            return FacturaCabecera.objects.filter(fecha__month=month, fecha__year=year, emisor=emis)
        except BaseException as ex:
            return ex
        
    def list_to_range_date(start = str, end = str, emisor_id= int):
        try:
            emis = Emisor.objects.get(_id=emisor_id)
            return FacturaCabecera.objects.filter(fecha__range=[start, end], emisor = emis)
        except BaseException as ex:
            return ex
    
class FacturaDetalle(models.Model):
    _id = models.AutoField(db_column="det_id", primary_key=True, verbose_name="Id")
    _cantidad = models.FloatField(db_column="det_cantidad",null=False, blank=False, default=0.00, verbose_name="Cantidad")
    _valorUnitario = models.FloatField(db_column="det_v_unitario",null=False, blank=False, default=0.00, verbose_name="Valor unitario")
    _descuento = models.FloatField(db_column="det_descuento", null=False, blank=False, default=0.00, verbose_name="Descuento")
    _ice = models.FloatField(db_column="det_ice", null=False, blank=False, default=0.00, verbose_name="ICE")
    _valorTotal = models.FloatField(db_column="det_total", null=False, blank=False, default=0.00, verbose_name="Total")
    _irbpnr = models.FloatField(db_column="det_irbpnr", null=False, blank=False, default=0.00, verbose_name="IRBPNR")
    _factura = models.ForeignKey(FacturaCabecera, db_column="det_factura", on_delete=models.CASCADE, verbose_name="Factura cabecera")
    _producto = models.ForeignKey(Producto, db_column="det_producto", on_delete=models.CASCADE, verbose_name="Producto")    
    _usuario = models.ForeignKey(User, db_column="det_usuario", on_delete=models.CASCADE, verbose_name="Usuario")
    
    def __str__(self):
        return str(self._id)
    
    class Meta:
        verbose_name = "Factura detalle"
        verbose_name_plural = "Facturas detalle"
        
    def create(facturaDetalle):
        try:
            facturaDetalle.save()
            return facturaDetalle._id
        except BaseException as ex:
            return ex
        
    def update(facturaDetalle):
        try:
            FacturaDetalle.objects.filter(_id=facturaDetalle.id)\
            .update(_cantidad = facturaDetalle.cantidad, _valorUnitario = facturaDetalle.valorUnitario\
            , _descuento = facturaDetalle.descuento, _ice = facturaDetalle.ice, _valorTotal = facturaDetalle.ice\
            , _valorTotal = facturaDetalle._valorTotal, _irbpnr = facturaDetalle._irbpnr, _factura = facturaDetalle._factura\
            , _producto = facturaDetalle._producto, _usuario = facturaDetalle._usuario)
            return True
        except BaseException as ex:
            return ex
        
    def search(id):
        try:
            return FacturaDetalle.objects.get(_id=id)
        except BaseException as ex:
            return ex
        
    def remove(id):
        try:
            FacturaDetalle.objects.filter(_id=id).delete()
            return True
        except BaseException as ex:
            return ex
        
    def list_to_cabecera(cabecera_id):
        """
        Method for list details to Cabecera.
        cabecera_id: Id de la Factura Cabecera.
        """
        try:
            return FacturaDetalle.objects.filter(_factura = cabecera_id)
        except BaseException as ex:
            return ex
        
class NotaDebito(models.Model):
    TYPE_COMPROBANTES = (
        ("01","Factura")
        )
    ESTADOS = (
        (1,"Generado"),
        (2,"Anulado"))
    
    _id = models.CharField(db_column="nde_id", primary_key=True, verbose_name="Id")
    _establecimiento = models.ForeignKey(Establecimiento, db_column="nde_est", on_delete=models.CASCADE, verbose_name="Establecimiento")
    _puntoEmision = models.ForeignKey(PuntoEmision, db_column="nde_p_emision", on_delete=models.CASCADE, verbose_name="Punto emisión")
    _secuencia = models.IntegerField(db_column="nde_secuencia", null=False, blank=False, verbose_name="Secuencia")
    _autorizacion = models.CharField(db_column="nde_autorizacion", maxlength=49, null=False, blank=False, verbose_name="Autorización")
    _claveacceso = models.CharField(db_column="nde_claveacceso", maxlength=49, null=False, blank = False, verbose_name="Clave de acceso")
    _fecha = models.DateField(db_column="nde_fecha", null=False, blank=False, verbose_name="Fecha")
    _comprobanteModificado = models.CharField(db_column="nde_comprobante", max_length=5, null=False, blank=False, choose=TYPE_COMPROBANTES ,verbose_name="Comprobante")
    _establecimientoDoc = models.CharField(db_column="nde_comprobante", max_length=3, null=False, blank = False, default="001", verbose_name="Est. Comprobante")
    _puntoEmisionDoc = models.CharField(db_column="nde_p_emi_comprobante", max_length=3, null=False, blank = False, default = "001", verbose_name="Punto emisión comprobante")
    _secuenciaDoc = models.CharField(db_column="nde_secuencia_doc", max_length=9, null=False, blank=False, default="000000001", verbose_name="Secuencia comprobante")
    _tarifa0 = models.FloatField(db_column="nde_tarifa0", null=False, blank=False, default = 0.00, verbose_name="Tarifa 0%")
    _tarifadif0 = models.FloatField(db_column="nde_tarifadif0", null=False, blank = False, default = 0.00, verbose_name = "Tarifa diferente 0%")
    _noObjetoIva = models.FloatField(db_column="nde_no_objeto", null=False, blank = False, default = 0.00, verbose_name = "No objeto IVA")
    _excento = models.FloatField(db_column="nde_excento", null=False, blank=False, default = 0.00, verbose_name="Excento")
    _valorIce = models.FloatField(db_column="nde_ice`", null=False, blank=False, default = 0.00, verbose_name="Valor ICE")
    _iva = models.FloatField(db_column="nde_iva", null=False, blank=False, default=0.00, verbose_name="IVA")
    _total = models.FloatField(db_column="nde_total", null=False, blank=False, default =0.00, verbose_name = "Total")
    _estado = models.IntegerField(db_column="nde_estado", null=False, blank=False, default = 1, choose = ESTADOS ,verbose_name = "Estado")
    _emisor = models.ForeignKey(Emisor, db_column="nde_emisor", on_delete=models.CASCADE, verbose_name="Emisor")
    _cliente = models.ForeignKey(Cliente, db_column="nde_cliente", on_delete=models.PROTECT, verbose_name="Cliente")
    _usuario = models.ForeignKey(User, db_column="nde_usuario", on_delete=models.PROTECT, verbose_name = "Usuario")
    
    
    def __str__(self):
        return str(self._id)
    
    class Meta:
        verbose_name = "Nota de Débito"
        verbose_name_plural = "Notas de Débito"
        
    def create(notadebito):
        try:
            nd = None
            try:
                #Realiza busqueda de la nota de debito, para verificar si ya se encuentra registrada.
                nd = NotaDebito.objects.filter(_establecimiento = notadebito._establecimiento, _puntoEmision=notadebito._puntoEmision, _secuencia = notadebito._secuencia, _emisor = notadebito._emisor)
            except Exception as e:
                print("Error en busqueda")
            if nd==None:
                notadebito.save()
                return notadebito._id
            else:
                return "La nota de debito ya esta registrada."
        except BaseException as ex:
            return ex
    def search_id(id=int):
        try:
            return NotaDebito.objects.filter(_id = id)
        except BaseException as ex:
            return ex
    
    def search(estab = str, p_emi=str, sec=str, emisor_id=int):
        """
        estab: Establecimiento Nota de Debito
        p_emi: Punto de PuntoEmision Nota de Debito
        sec: Secuencia de Nota de Debito
        emisor_id: Id del emisor de la nota de debito.
        """
        try:
            return NotaDebito.objects.filter(_establecimiento = estab, _puntoEmision = p_emi, _secuencia = sec, _emisor=emisor_id)
        except BaseException as ex:
            return ex
        
    
    def update(notadebito):
        try:
            NotaDebito.objects.filter(_id=notadebito.id).update(_establecimiento=notadebito._establecimiento
            ,_puntoEmision =notadebito._puntoEmision
            ,_secuencia=notadebito._secuencia
            ,_autorizacion=notadebito._autorizacion
            ,_claveacceso=notadebito._claveacceso
            ,_fecha=notadebito._fecha
            ,_comprobanteModificado=notadebito._comprobanteModificado
            ,_establecimientoDoc=notadebito._establecimientoDoc
            ,_puntoEmisionDoc=notadebito._puntoEmisionDoc
            ,_secuenciaDoc=notadebito._secuenciaDoc
            ,_tarifa0=notadebito._tarifa0
            ,_tarifadif0=notadebito._tarifadif0
            ,_noObjetoIva=notadebito._noObjetoIva
            ,_excento=notadebito._excento
            ,_valorIce=notadebito._valorIce
            ,_iva=notadebito._iva
            ,_total=notadebito._total
            ,_estado=notadebito._estado
            ,_emisor=notadebito._emisor
            ,_cliente=notadebito._cliente
            ,_usuario=notadebito._usuario)
            return True
        except BaseException as ex:
            return ex
    def remove(id=int):
        try:
            NotaDebito.objects.filter(_id=id).delete()
            return True
        except BaseException as ex:
            return ex
    
    def list_to_emisor(emisor_id=int, start=str, end=str):
        try:
            return NotaDebito.objects.filter(_emisor=emisor_id, _fecha__range=[start, end])
        except BaseException as ex:
            return ex
    
    
class FormaPago(models.Model):
    _id = models.AutoField(db_column="fpa_id",primary_key=True, verbose_name="Id")
    _codigo = models.CharField(db_column="fpa_codigo", null=False, blank=True, default="", verbose_name="Código")
    _descripcion = models.CharfField(db_column="fpa_descripcion", null=False, blank=True, default="", verbose_name="Descripción")
    _valor = models.FloatField(db_column="fpa_valor", null=False, blank=False, default = 0.00, verbose_name="Valor")
    _plazo = models.IntegerField(db_column="fpa_plazo", null=False, blank=False, default = 0.00, verbose_name="Plazo")
    _tiempo = models.IntegerField(db_column="fpa_tiempo", null=False, blank=False, default = 0.00, verbose_name="Tiempo")
    _factura = models.ForeignKey(FacturaCabecera, db_column="fpa_factura", null=True, blank=True, verbose_name="Factura")
    _notaDebito = models.ForeignKey(NotaDebito, db_column="fpa_nota_debito", null=True, blank=True, verbose_name="Nota debito")
    _usuario = models.ForeignKey(User, db_column="fpa_usuario", verbose_name="Usuario")
    
    def __str__(self):
        return str(self._id)
    
    class Meta:
        verbose_name = "Nota de débito"
        verbose_name_plural = "Notas de débito"
        
    
    