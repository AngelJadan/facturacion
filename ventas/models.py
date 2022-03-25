from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Emisor(models.Model):
    TYPE_ID = (
        ("01", "RUC"),
        ("05", "Cedula"),
    )
    TYPE_AMB = (
        ("01", "Pruebas"),
        ("02", "Producción"),)

    id = models.AutoField(
        db_column='emi_id', primary_key=True, verbose_name="Id")
    identificacion = models.CharField(db_column="emi_identificacion", unique=True,
                                      max_length=20, null=False, blank=False, verbose_name="Identificacion")
    tipo_id = models.CharField(db_column="emi_tipo_id", null=False, blank=False,
                               max_length=5, choices=TYPE_ID, default="01", verbose_name="Tipo")
    rasonSocial = models.CharField(db_column="emi_razon_social", max_length=500,
                                   null=False, blank=False, unique=True, default="sn", verbose_name="Razón social")
    nombreComercial = models.CharField(db_column="emi_nombre_comercial", max_length=255,
                                       null=True, blank=True, unique=True, default="sn", verbose_name="Nombre comercial")
    telefono = models.CharField(db_column="emi_telefono", max_length=20,
                                null=True, blank=True, default="sn", verbose_name="Telefono")
    direccionMatriz = models.CharField(db_column="emi_direccion_matriz", max_length=255,
                                       null=True, blank=True, default="sn", verbose_name="Dirección matriz")
    contribuyenteEspecial = models.CharField(
        db_column="emi_contribuyente", max_length=50, null=True, blank=True, default="sn", verbose_name="Contribuyente especial")
    obligadoLlevarContabilidad = models.BooleanField(
        db_column="emi_obligado", null=False, blank=False, default=False, verbose_name="Obligado")
    regimenMicroempresa = models.BooleanField(
        db_column="emi_regimen_microempresa", null=False, blank=False, default=False, verbose_name="Microempresa")
    agenteRetencion = models.BooleanField(
        db_column="emi_agente_retencion", null=False, blank=False, default=False, verbose_name="Agente de retención")
    logo = models.CharField(db_column="emi_logo", max_length=250,
                            null=True, blank=True, default="", verbose_name="Logo")
    ambiente = models.CharField(
        db_column="emi_ambiente", max_length=2, null=False, blank=False, default="Prueba", choices=TYPE_AMB, verbose_name="Ambiente")
    tipoToken = models.CharField(
        db_column="emi_tipo_token", max_length=100, null=False, blank=False, default="", verbose_name="Tipo token")
    firma = models.CharField(db_column="emi_firma", max_length=500,
                             null=False, blank=False, verbose_name="Firma")
    estado = models.IntegerField(
        db_column="emi_estado", null=False, blank=False, verbose_name="Estado")
    cantidad_usuario = models.IntegerField(
        db_column="emi_cantidad_user", null=False, blank=False, default=1, verbose_name="Cantidad de usuarios")
    usuario = models.ForeignKey(User, db_column="emi_usuario",
                                on_delete=models.CASCADE, null=False, blank=False, verbose_name="Usuario")

    def __str__(self):
        return f'{self.identificacion}'

    class Meta:
        verbose_name = "Emisor"
        verbose_name_plural = "Emisores"

    def validarIdentificacion(_identificacion):
        try:
            l = len(_identificacion)
            if l == 10 or l == 13:  # verificar la longitud correcta
                cp = int(_identificacion[0:2])
                if cp >= 1 and cp <= 22:  # verificar codigo de provincia
                    tercer_dig = int(_identificacion[2])
                    if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                        if l == 10:
                            return __validar_ced_ruc(_identificacion, 0)
                        elif l == 13:
                            # se verifica q los ultimos numeros no sean 000
                            return __validar_ced_ruc(_identificacion, 0) and _identificacion[10:13] != '000'
                    elif tercer_dig == 6:
                        # sociedades publicas
                        return __validar_ced_ruc(_identificacion, 1)
                    elif tercer_dig == 9:  # si es ruc
                        # sociedades privadas
                        return __validar_ced_ruc(_identificacion, 2)
                    else:
                        raise Exception(u'Tercer digito invalido')
                else:
                    raise Exception(u'Codigo de provincia incorrecto')
            else:
                raise Exception(u'Longitud incorrecta del numero ingresado')
        except BaseException as ex:
            return ex

    def __validar_ced_ruc(nro, tipo):
        total = 0
        if tipo == 0:  # cedula y r.u.c persona natural
            base = 10
            d_ver = int(nro[9])  # digito verificador
            multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
        elif tipo == 1:  # r.u.c. publicos
            base = 11
            d_ver = int(nro[8])
            multip = (3, 2, 7, 6, 5, 4, 3, 2)
        elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
            base = 11
            d_ver = int(nro[9])
            multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
        for i in range(0, len(multip)):
            p = int(nro[i]) * multip[i]
            if tipo == 0:
                total += p if p < 10 else int(str(p)[0])+int(str(p)[1])
            else:
                total += p
        mod = total % base
        val = base - mod if mod != 0 else 0
        return val == d_ver

    def crearEmisor(emisor):
        try:
            emisor.save()
            return emisor
        except BaseException as ex:
            return ex

    def search(identificacion=str):
        try:
            return Emisor.objects.filter(identificacion=identificacion)
        except BaseException as ex:
            return ex

    def search_id(id=int):
        try:
            return Emisor.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def actualizarEmisor(emisor):
        try:
            Emisor.objects.filter(id=emisor.id).update(identificacion=emisor.identificacion, tipo_id=emisor.tipo_id, rasonSocial=emisor.rasonSocial, nombreComercial=emisor.nombreComercial, telefono=emisor.telefono, direccionMatriz=emisor.direccionMatriz, contribuyenteEspecial=emisor.contribuyenteEspecial,
                                                       obligadoLlevarContabilidad=emisor.obligadoLlevarContabilidad, regimenMicroempresa=emisor.regimenMicroempresa, agenteRetencion=emisor.agenteRetencion, logo=emisor.logo, ambiente=emisor.ambiente, tipoToken=emisor.tipoToken, firma=emisor.firma, estado=emisor.estado, usuario=emisor.usuario)
            return True
        except BaseException as ex:
            return ex


class User_Emisor(models.Model):
    id = models.AutoField(
        db_column='use_id', primary_key=True, verbose_name="Id")
    emisor = models.ForeignKey(
        Emisor, db_column="use_emisor", verbose_name="Emisor", on_delete=models.PROTECT)
    user = models.OneToOneField(
        User, db_column="use_user", on_delete=models.CASCADE, verbose_name="Usuario")
    estado = models.BooleanField(
        db_column="use_estado", default=False, verbose_name="Estado")

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

    def update(user_emisor):
        try:
            User_Emisor.objects.filter(id=user_emisor.id).update(
                emisor=user_emisor.emisor, estado=user.user_emisor.estado)
            return True
        except BaseException as ex:
            return ex

    def search(id):
        try:
            return User_Emisor.objects.get(id=id)
        except BaseException as ex:
            return ex


class Establecimiento(models.Model):
    id = models.AutoField(
        db_column="est_id", primary_key=True, verbose_name="Id")
    serie = models.CharField(db_column="est_serie", max_length=3,
                             null=False, blank=False, default="001", verbose_name="Serie")
    nombre = models.CharField(db_column="est_nombre", max_length=250,
                              null=True, blank=True, default="Sn", verbose_name="Nombre")
    telefono = models.CharField(db_column="est_telefono", max_length=250,
                                null=True, blank=True, default="Sn", verbose_name="Teléfono")
    direccion = models.CharField(db_column="est_direccion", max_length=250,
                                 null=True, blank=True, default="Sn", verbose_name="Dirección")
    emisor = models.ForeignKey(Emisor, db_column="est_emisor",
                               on_delete=models.CASCADE, verbose_name="Emisor")
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="est_usuario", verbose_name="Usuario")

    class Meta:
        verbose_name = "Establecimiento"
        verbose_name_plural = "Establecimientos"

    def __str__(self):
        return str(self.id)

    def create(establecimiento):
        try:
            est = None
            for est_temp in Establecimiento.objects.filter(serie=establecimiento.serie, emisor=establecimiento.emisor):
                est = est_temp
            if est==None:
                establecimiento.save()
                return establecimiento
            else:
                return "Ya existe un establecimiento con esta serie"
            
        except BaseException as ex:
            return ex

    def update(establecimiento):
        try:
            Establecimiento.objects.filter(id=establecimiento.id).update(
                serie=establecimiento.serie,
                nombre=establecimiento.nombre,
                telefono=establecimiento.telefono,
                direccion=establecimiento.direccion,
                emisor=establecimiento.emisor,
                usuario=establecimiento.usuario,
            )
            return True
        except BaseException as ex:
            return ex
    def search_id(id):
        try:
            return Establecimiento.objects.get(id=id)
        except BaseException as ex:
            return ex

    def remove(id):
        try:
            Establecimiento.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_emisor(emisor_id=int):
        try:
            return Establecimiento.objects.filter(emisor=emisor_id)
        except BaseException as ex:
            return ex


class PuntoEmision(models.Model):
    id = models.AutoField(
        db_column="pem_id", primary_key=True, verbose_name="Id")
    serie = models.CharField(db_column="pem_serie", max_length=3,
                             null=False, blank=False, default="001", verbose_name="Serie")
    descripcion = models.CharField(db_column="pem_descripcion", max_length=250,
                                   null=False, blank=False, default="sn", verbose_name="Descripción")
    establecimiento = models.ForeignKey(
        Establecimiento, db_column="pem_establecimiento", related_name="puntos_emision", on_delete=models.PROTECT, verbose_name="Establecimiento")
        #Establecimiento, db_column="pem_establecimiento", on_delete=models.PROTECT, verbose_name="Establecimiento")
    estado = models.BooleanField(
        db_column="pem_estado", null=False, blank=False, default=False, verbose_name="Estado")
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, db_column="pem_usuario", verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Punto de emisión"
        verbose_name_plural = "Puntos de emisión"

    def create(puntoEmision):
        try:
            pemi_temp = None
            print("serie ", puntoEmision.serie, " est ", puntoEmision.establecimiento)
            for punto in PuntoEmision.objects.filter(serie=puntoEmision.serie, establecimiento=puntoEmision.establecimiento):
                pemi_temp = punto
            
            print("pemi_temp ",pemi_temp)
            if pemi_temp == None:
                puntoEmision.save()
                return puntoEmision
            else:
                return "El punto de emision con esta serie ya existe en este emisor."
        except BaseException as ex:
            return ex

    def update(punto_emision):
        try:
            PuntoEmision.objects.filter(id=punto_emision.id).update(
                serie=punto_emision.serie,
                descripcion=punto_emision.descripcion,
                establecimiento=punto_emision.establecimiento,
                estado=punto_emision.estado,
                usuario=punto_emision.usuario
            )
            return True
        except BaseException as ex:
            return ex

    def search_id(id=int):
        try:
            return PuntoEmision.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def remove(id=int):
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
    TYPE_ID = (
        ("05", "Cédula"),)

    id = models.AutoField(
        db_column="cli_id", primary_key=True, verbose_name="Id")
    nombreApellido = models.CharField(
        db_column="cli_nombre_apellido", max_length=250, null=False, blank=False, verbose_name="Nombre y Apellido", default="sn")
    identificacion = models.CharField(
        db_column="cli_identificacion", max_length=20, null=False, blank=False, verbose_name="Identificacion")
    tipoIdentificacion = models.CharField(db_column="cli_tipo_identificacion", max_length=5, default="sn",
                                          null=False, blank=False, choices=TYPE_ID, verbose_name="Tipo de identificación")
    direccion = models.CharField(db_column="cli_direccion", max_length=250,
                                 null=False, blank=False, default="Sn", verbose_name="Dirección")
    telefono = models.CharField(db_column="cli_telefono", max_length=20,
                                null=False, blank=False, default="Sn", verbose_name="Telefono")
    extension = models.CharField(db_column="cli_extension", max_length=10,
                                 null=True, blank=True, default="sn", verbose_name="Extension")
    movil = models.CharField(db_column="cli_movil", max_length=15,
                             null=True, blank=True, default="sn", verbose_name="Movil")
    mail = models.EmailField(
        db_column="cli_mail", max_length=250, null=False, blank=False, default="sn", verbose_name="Mail")
    usuario = models.ForeignKey(
        User, db_column="cli_usuario", on_delete=models.PROTECT, verbose_name="Usuario")
    emisor = models.ForeignKey(
        Emisor, db_column="cli_emisor", on_delete=models.PROTECT, verbose_name="Emisor")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def create(cliente):
        try:
            cliente.save()
            return cliente._id
        except BaseException as ex:
            return ex

    def update(cliente):
        try:
            Cliente.objects.filter(id=cliente.id).update(
                nombreApellido=cliente.nombreApellido,
                identificacion=cliente.identificacion,
                tipoIdentificacion=cliente.tipoIdentificacion,
                direccion=cliente.direccion,
                telefono=cliente.telefono,
                extension=cliente.extension,
                movil=cliente.movil,
                mail=cliente.mail,
                usuario=cliente.usuario,
                emisor=cliente.emisor,
            )
            return True
        except BaseException as ex:
            return ex

    def search(id):
        try:
            return Cliente.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def remove(id):
        try:
            Cliente.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list(emisor_id=int):
        try:
            return Cliente.objects.filter(emisor=emisor_id)
        except BaseException as ex:
            return ex


class Iva(models.Model):
    id = models.AutoField(db_column="iva_id", primary_key=True)
    descripcion = models.CharField(
        db_column="iva_descripcion", max_length=250, null=True, blank=True, default="", verbose_name='Descripción')
    porcentaje = models.FloatField(
        db_column="iva_porcentaje", null=False, blank=False, default=0.00, unique=True, verbose_name='Porcentaje')
    user = models.ForeignKey(
        User, db_column="iva_user", on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "IVA"
        verbose_name_plural = "IVAs"

    def create(iva):
        try:
            iva.save()
            return iva._id
        except BaseException as ex:
            return ex
        
    def update(iva):
        try:
            Iva.objects.filter(id=iva.id).update(descripcion=iva.descripcion,
                                                porcentaje=iva.porcentaje,
                                                user=iva.user)
            return True
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return Iva.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def remove(id=int):
        try:
            Iva.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list():
        try:
            return Iva.objects.all().order_by("porcentaje")
        except BaseException as ex:
            return ex

        
class Producto(models.Model):
    id = models.AutoField(
        db_column='pro_id', primary_key=True, verbose_name="Id")
    nombre = models.CharField(
        db_column='pro_nombre', max_length=250, null=False, blank=False, unique=True, verbose_name="Nombre")
    codigoPrincipal = models.CharField(
        db_column='pro_principal', max_length=20, null=False, blank=False, unique=True, verbose_name="Código principal")
    codigoAuxiliar = models.CharField(
        db_column='pro_auxiliar', max_length=20, null=False, blank=False, unique=True, verbose_name="Código auxiliar")
    tipo = models.CharField(
        db_column='pro_tipo', max_length=20, null=False, blank=False, verbose_name="Tipo")
    ice = models.FloatField(
        db_column="pro_ice", null=False, blank=False, verbose_name="ICE")
    irbpnr = models.FloatField(
        db_column="pro_irbpnr", null=False, blank=False, verbose_name="IRBPNR")
    precio1 = models.FloatField(
        db_column="pro_precio1", null=False, blank=False, default=0.00, verbose_name="Precio 1")
    precio2 = models.FloatField(
        db_column="pro_precio2", null=False, blank=False, default=0.00, verbose_name="Precio 2")
    precio3 = models.FloatField(
        db_column="pro_precio3", null=False, blank=False, default=0.00, verbose_name="Precio 3")
    precio4 = models.FloatField(
        db_column="pro_precio4", null=False, blank=False, default=0.00, verbose_name="Precio 4")
    iva = models.ForeignKey(Iva, db_column="pro_iva",
                            on_delete=models.PROTECT, verbose_name="IVA")
    descripcion = models.CharField(
        db_column="pro_descripcion", max_length=255, null=False, blank=True, default="", verbose_name="Descripción")
    emisor = models.ForeignKey(
        Emisor, db_column="pro_emisor", on_delete=models.PROTECT, verbose_name="Emisor")
    usuario = models.ForeignKey(
        User, db_column="pro_usuario", on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def create(producto):
        try:
            producto.save()
            return producto.id
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return Producto.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def update(producto):
        try:
            Producto.objects.filter(id=producto.id).update(nombre=producto.nombre, codigoPrincipal=producto.codigoPrincipal, codigoAuxiliar=producto._codigoAuxiliar, _tipo=producto._tipo, ice=producto.ice, irbpnr=producto.irbpnr,
                                                            precio1=producto.precio1, precio2=producto.precio2, precio3=producto.precio3, _precio4=producto._precio4, _iva=producto._iva, _descripcion=producto.descripcion, emisor=producto.emisor, usuario=producto.usuario)
            return True
        except BaseException as e:
            return e

    def remove(id=int):
        try:
            Producto.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_emisor(id_emisor=int):
        try:
            return Producto.objects.filter(emisor=id_emisor)
        except BaseException as ex:
            return ex


class FacturaCabecera(models.Model):
    id = models.AutoField(
        db_column="fac_id", primary_key=True, verbose_name="Id")
    establecimiento = models.ForeignKey(
        Establecimiento, db_column="fac_establecimiento", on_delete=models.CASCADE, verbose_name="Establecimiento")
    punto_emision = models.ForeignKey(
        PuntoEmision, db_column="fac_punto_emision", on_delete=models.CASCADE, verbose_name="Punto de emision")
    secuencia = models.IntegerField(
        db_column="fac_secuencia", null=False, blank=False, verbose_name="Secuencia")
    autorizacion = models.CharField(db_column="fac_autorizacion", max_length=49,
                                    null=False, blank=False, verbose_name="Autorizacion", default="999")
    claveacceso = models.CharField(db_column="fac_claveacceso", max_length=49,
                                   null=False, blank=False, verbose_name="Clave de acceso", default="999")
    fecha = models.DateField(db_column="fac_fecha",
                             null=False, blank=False, verbose_name="Fecha")
    emisor = models.ForeignKey(
        Emisor, db_column="fac_emisor", on_delete=models.CASCADE, verbose_name="Emisor")
    cliente = models.ForeignKey(
        Cliente, db_column="fac_cliente", on_delete=models.CASCADE, verbose_name="Cliente")
    establecimientoGuia = models.CharField(
        db_column="fact_est_guia", max_length=3, null=True, blank=True, default=None, verbose_name="Est. Guia")
    puntoGuia = models.CharField(db_column="fac_punto_guia", max_length=3,
                                 null=True, blank=True, default=None, verbose_name="Punto de emisión")
    secuenciaGuia = models.CharField(db_column="fac_secuencia_guia", max_length=9,
                                     null=True, blank=True, default=None, verbose_name="Secuencia de guia")
    noobjetoiva = models.FloatField(
        db_column="fac_no_objetoiva", null=False, blank=False, default=0.00, verbose_name="No objeto de IVA")
    tarifa0 = models.FloatField(
        db_column="fac_tarifa0", null=False, blank=False, default=0.00, verbose_name="Tafira 0%")
    tarifadif0 = models.FloatField(
        db_column="fac_tarifadif0", null=False, blank=False, default=0.00, verbose_name="Tafira diferente 0%")
    excentoiva = models.FloatField(
        db_column="fac_excento", null=False, blank=False, default=0.00, verbose_name="Excento IVA")
    totaldescuento = models.FloatField(
        db_column="fac_total_descuento", null=False, blank=False, default=0.00, verbose_name="Total descuento")
    totalice = models.FloatField(
        db_column="fac_total_ice", null=False, blank=False, default=0.00, verbose_name="Total ICE")
    totalirbpnt = models.FloatField(
        db_column="fac_total_irbpnt", null=False, blank=False, default=0.00, verbose_name="Total IRBPNT")
    iva = models.ForeignKey(Iva, db_column="fac_iva",
                            on_delete=models.CASCADE, verbose_name="IVA")
    valorIva = models.FloatField(
        db_column="fac_valor_iva", null=False, blank=False, default=0.00, verbose_name="Valor iva")
    propina = models.FloatField(
        db_column="fac_propina", null=False, blank=False, default=0, verbose_name="Propina")
    total = models.FloatField(
        db_column="fac_total", null=False, blank=False, default=0.00, verbose_name="Total")
    estado = models.BooleanField(
        db_column="fac_estado", null=False, blank=False, default=True, verbose_name="Estado")
    usuario = models.ForeignKey(
        User, db_column="fac_usuario", on_delete=models.PROTECT, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def create(factura):
        try:
            factura.save()
            return factura.id
        except BaseException as ex:
            return ex


    def search_to_id(id=int):
        try:
            return FacturaCabecera.objects.filter(id=id)
        except BaseException as ex:
            return ex
    def get_numero_secuencia(establecimiento=int, punto_emision=int ,emisor_id=int,):
        """
        establecimiento: Id del establecimiento.
        punto_emision: Id del punto de emision.
        emisor_id: 
        
        return: Metodo para obtener el ultimo numero de secuencia de la factura.
        """
        try:
            return FacturaCabecera.objects.filter(emisor=emisor_id, establecimiento=establecimiento,punto_emision=punto_emision).order_by("+secuencia")[0]
            
        except BaseException as ex:
            return ex
        

    def search_to_factura(establecimiento=str, punto_emision=str, secuencia=str, emisor_id=int):
        """
        establcimiento: Serie de establecimiento ejemplo 001
        punto_emision: Serie de punto de emision ejemplo 002
        secuencia: Numero de secuencia de la factura
        emisor_id :Id del emisor.
        
        """
        est = None
        p_emi = None
        emis = None

        try:
            est = Establecimiento.objects.get(serie=establecimiento)
            p_emi = PuntoEmision.objects.get(serie=punto_emision)
            emis = Emisor.objects.get(id=emisor_id)

            if est != None and p_emi != None and emis != None:
                return FacturaCabecera.objects.filter(establecimiento=est, punto_emision=p_emi, secuencia=secuencia, emisor=emis)
            else:
                return []

        except BaseException as ex:
            return ex

    def remove(id=int):
        try:
            FacturaCabecera.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_month_year(month=str, year=str, emisor_id=int):
        try:
            emis = Emisor.objects.get(id=emisor_id)
            return FacturaCabecera.objects.filter(fecha__month=month, fecha__year=year, emisor=emis)
        except BaseException as ex:
            return ex

    def list_to_range_date(start=str, end=str, emisor_id=int):
        try:
            emis = Emisor.objects.get(id=emisor_id)
            return FacturaCabecera.objects.filter(fecha__range=[start, end], emisor=emis)
        except BaseException as ex:
            return ex


class FacturaDetalle(models.Model):
    id = models.AutoField(
        db_column="det_id", primary_key=True, verbose_name="Id")
    cantidad = models.FloatField(
        db_column="det_cantidad", null=False, blank=False, default=0.00, verbose_name="Cantidad")
    valorUnitario = models.FloatField(
        db_column="det_v_unitario", null=False, blank=False, default=0.00, verbose_name="Valor unitario")
    descuento = models.FloatField(
        db_column="det_descuento", null=False, blank=False, default=0.00, verbose_name="Descuento")
    ice = models.FloatField(
        db_column="det_ice", null=False, blank=False, default=0.00, verbose_name="ICE")
    valorTotal = models.FloatField(
        db_column="det_total", null=False, blank=False, default=0.00, verbose_name="Total")
    irbpnr = models.FloatField(
        db_column="det_irbpnr", null=False, blank=False, default=0.00, verbose_name="IRBPNR")
    factura = models.ForeignKey(FacturaCabecera, db_column="det_factura",
                                related_name="facturaDetalle", on_delete=models.CASCADE, verbose_name="Factura cabecera")
    producto = models.ForeignKey(
        Producto, db_column="det_producto", on_delete=models.CASCADE, verbose_name="Producto")
    usuario = models.ForeignKey(
        User, db_column="det_usuario", on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

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
            FacturaDetalle.objects.filter(id=facturaDetalle.id)\
                .update(cantidad=facturaDetalle.cantidad, valorUnitario=facturaDetalle.valorUnitario, descuento=facturaDetalle.descuento, ice=facturaDetalle.ice, valorTotal=facturaDetalle.valorTotal, irbpnr=facturaDetalle.irbpnr, factura=facturaDetalle.factura, producto=facturaDetalle.producto, usuario=facturaDetalle.usuario)
            return True
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return FacturaDetalle.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def remove(id=int):
        try:
            FacturaDetalle.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_cabecera(cabecera_id):
        """
        Method for list details to Cabecera.
        cabecera_id: Id de la Factura Cabecera.
        """
        try:
            return FacturaDetalle.objects.filter(factura=cabecera_id)
        except BaseException as ex:
            return ex


class NotaDebito(models.Model):
    TYPE_COMPROBANTES = (
        ("01", "Factura"),
    )
    ESTADOS = (
        ("1", "Generado"),
        ("2", "Anulado"))

    id = models.AutoField(
        db_column="nde_id", primary_key=True, verbose_name="Id")
    establecimiento = models.ForeignKey(
        Establecimiento, db_column="nde_est", on_delete=models.CASCADE, verbose_name="Establecimiento")
    puntoEmision = models.ForeignKey(
        PuntoEmision, db_column="nde_p_emision", on_delete=models.CASCADE, verbose_name="Punto emisión")
    secuencia = models.IntegerField(
        db_column="nde_secuencia", null=False, blank=False, verbose_name="Secuencia")
    autorizacion = models.CharField(
        db_column="nde_autorizacion", max_length=49, null=False, blank=False, verbose_name="Autorización")
    claveacceso = models.CharField(
        db_column="nde_claveacceso", max_length=49, null=False, blank=False, verbose_name="Clave de acceso")
    fecha = models.DateField(db_column="nde_fecha",
                             null=False, blank=False, verbose_name="Fecha")
    comprobanteModificado = models.CharField(
        db_column="nde_comprobante", max_length=5, null=False, blank=False, choices=TYPE_COMPROBANTES, verbose_name="Comprobante")
    establecimientoDoc = models.CharField(
        db_column="nde_comprobante_doc", max_length=3, null=False, blank=False, default="001", verbose_name="Est. Comprobante")
    puntoEmisionDoc = models.CharField(db_column="nde_p_emi_comprobante", max_length=3,
                                       null=False, blank=False, default="001", verbose_name="Punto emisión comprobante")
    secuenciaDoc = models.CharField(db_column="nde_secuencia_doc", max_length=9,
                                    null=False, blank=False, default="000000001", verbose_name="Secuencia comprobante")
    tarifa0 = models.FloatField(
        db_column="nde_tarifa0", null=False, blank=False, default=0.00, verbose_name="Tarifa 0%")
    tarifadif0 = models.FloatField(db_column="nde_tarifadif0", null=False,
                                   blank=False, default=0.00, verbose_name="Tarifa diferente 0%")
    noObjetoIva = models.FloatField(
        db_column="nde_no_objeto", null=False, blank=False, default=0.00, verbose_name="No objeto IVA")
    excento = models.FloatField(
        db_column="nde_excento", null=False, blank=False, default=0.00, verbose_name="Excento")
    valorIce = models.FloatField(
        db_column="nde_ice`", null=False, blank=False, default=0.00, verbose_name="Valor ICE")
    iva = models.FloatField(
        db_column="nde_iva", null=False, blank=False, default=0.00, verbose_name="IVA")
    total = models.FloatField(
        db_column="nde_total", null=False, blank=False, default=0.00, verbose_name="Total")
    estado = models.CharField(db_column="nde_estado", max_length=5, null=False,
                              blank=False, default="1", choices=ESTADOS, verbose_name="Estado")
    emisor = models.ForeignKey(
        Emisor, db_column="nde_emisor", on_delete=models.CASCADE, verbose_name="Emisor")
    cliente = models.ForeignKey(
        Cliente, db_column="nde_cliente", on_delete=models.PROTECT, verbose_name="Cliente")
    usuario = models.ForeignKey(
        User, db_column="nde_usuario", on_delete=models.PROTECT, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Nota de Débito"
        verbose_name_plural = "Notas de Débito"

    def create(notadebito):
        try:
            nd = None
            try:
                # Realiza busqueda de la nota de debito, para verificar si ya se encuentra registrada.
                nd = NotaDebito.objects.filter(establecimiento=notadebito.establecimiento,
                                               puntoEmision=notadebito.puntoEmision, secuencia=notadebito.secuencia, emisor=notadebito.emisor)
            except Exception as e:
                print("Error en busqueda")
            if nd == None:
                notadebito.save()
                return notadebito.id
            else:
                return "La nota de debito ya esta registrada."
        except BaseException as ex:
            return ex

    def search_id(id=int):
        try:
            return NotaDebito.objects.filter(_id=id)
        except BaseException as ex:
            return ex

    def search(estab=str, p_emi=str, sec=str, emisor_id=int):
        """
        estab: Establecimiento Nota de Debito
        p_emi: Punto de PuntoEmision Nota de Debito
        sec: Secuencia de Nota de Debito
        emisor_id: Id del emisor de la nota de debito.
        """
        try:
            return NotaDebito.objects.filter(_establecimiento=estab, _puntoEmision=p_emi, _secuencia=sec, _emisor=emisor_id)
        except BaseException as ex:
            return ex

    def update(notadebito):
        try:
            NotaDebito.objects.filter(id=notadebito.id).update(establecimiento=notadebito.establecimiento, puntoEmision=notadebito.puntoEmision, secuencia=notadebito.secuencia, autorizacion=notadebito.autorizacion, claveacceso=notadebito.claveacceso, fecha=notadebito.fecha, comprobanteModificado=notadebito.comprobanteModificado, establecimientoDoc=notadebito.establecimientoDoc,
                                                                puntoEmisionDoc=notadebito.puntoEmisionDoc, secuenciaDoc=notadebito.secuenciaDoc, tarifa0=notadebito.tarifa0, tarifadif0=notadebito.tarifadif0, noObjetoIva=notadebito.noObjetoIva, excento=notadebito.excento, valorIce=notadebito.valorIce, iva=notadebito.iva, total=notadebito.total, estado=notadebito.estado, emisor=notadebito.emisor, cliente=notadebito.cliente, usuario=notadebito.usuario)
            return True
        except BaseException as ex:
            return ex

    def remove(id=int):
        try:
            NotaDebito.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_emisor(emisor_id=int, start=str, end=str):
        try:
            return NotaDebito.objects.filter(emisor=emisor_id, fecha__range=[start, end])
        except BaseException as ex:
            return ex


class Otro(models.Model):
    id = models.AutoField(
        db_column="otr_id", primary_key=True, verbose_name="Id")
    nombre = models.CharField(
        db_column="otr_nombre", max_length=250, null=False, blank=False, verbose_name="Nombre")
    descripcion = models.CharField(
        db_column="otr_descripcion", max_length=250, null=False, blank=False, verbose_name="Descripción")
    factura = models.ForeignKey(
        FacturaCabecera, related_name="otro", db_column="otr_factura", on_delete=models.CASCADE, verbose_name="Factura")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Otro"
        verbose_name_plural = "Otros"

    def create(otro):
        try:
            otro.save()
            return otro._id
        except BaseException as ex:
            return ex
    def update(otro):
        try:
            Otro.objects.filter(id=id).update(nombre=otro.nombre, 
                                                     descripcion=otro.descripcion,
                                                     factura=otro.factura)
            return True
        except BaseException as ex:
            return ex

    def search(id):
        try:
            return Otro.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def remove(id):
        try:
            Otro.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_factura(id_factura):
        try:
            return Otro.objects.filter(factura=id_factura)
        except BaseException as ex:
            return ex


class FormaPago(models.Model):
    id = models.AutoField(
        db_column="fpa_id", primary_key=True, verbose_name="Id")
    codigo = models.CharField(
        db_column="fpa_codigo", unique=True, max_length=10, null=False, blank=True, default="", verbose_name="Código")
    descripcion = models.CharField(
        db_column="fpa_descripcion", max_length=255, null=False, blank=True, default="", verbose_name="Descripción")
    usuario = models.ForeignKey(
        User, db_column="fpa_usuario", on_delete=models.PROTECT, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Nota de débito"
        verbose_name_plural = "Notas de débito"

    def create(forma_pago):
        try:
            forma_pago.save()
            return forma_pago._id
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return FormaPago.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def update(forma_pago):
        try:
            FormaPago.objects.filter(id=forma_pago.id).update(codigo=forma_pago.codigo,
                                                            descripcion=forma_pago.descripcion,
                                                            usuario=forma_pago.usuario)
        except BaseException as ex:
            return ex

    def list_to_cliente():
        try:
            return FormaPago.objects.filter.all()
        except BaseException as ex:
            return ex


class FormaPagoFactura(models.Model):
    
    id = models.AutoField(db_column="fpf_id", primary_key=True, verbose_name="Id")
    formaPago = models.ForeignKey(
        FormaPago, db_column="fpf_forma_pago" , on_delete=models.PROTECT, verbose_name="Forma de pago"
    )
    facturaid = models.ForeignKey(
        FacturaCabecera, related_name="forma_pago_factura", db_column="fpf_factura", on_delete=models.PROTECT, verbose_name="Factura"
    )
    tiempo = models.IntegerField(db_column="fpf_tiempo", null=True, blank=True, verbose_name="Tiemmpo")
    plazo = models.IntegerField(db_column="fpf_plazo", null=True, blank=True, verbose_name = "Plazo")
    valor = models.FloatField(db_column="fpf_valor", null=True, blank=True, verbose_name="Valor")
    usuario = models.ForeignKey(
        User, db_column="fpf_usuario", on_delete= models.PROTECT
    )
    
    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name = "Forma de pago factura"
        verbose_name_plural = "Formas de pago de factura"
    
    
    def search_id(id=int):
        try:
            return FormaPagoFactura.objects.filter(id=id)
        except BaseException as ex:
            return ex
    
    def search_to_id_factura(id=int):
        try:
            return FormaPagoFactura.objects.filter(facturaid=id)
        except BaseException as ex:
            return ex
    
    def update(formaPagoFactura):
        try:
            FormaPagoFactura.objects.filter(id=formaPagoFactura).update(
                formaPago = formaPagoFactura.formaPago,
                facturaid = formaPagoFactura.facturaid,
                tiempo = formaPagoFactura.tiempo,
                plazo = formaPagoFactura.plazo,
                valor = formaPagoFactura.valor,
                usuario = formaPagoFactura.usuario
            )
            return True
        except BaseException as ex:
            return ex
    def remove(id=int):
        try:
            FormaPagoFactura.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex
    
class FormaPagoNotaDebito(models.Model):
    id = models.AutoField(db_column="fpn", primary_key=True, verbose_name="Id")
    nota_debito = models.ForeignKey(NotaDebito, db_column="fpn_nota_debito", on_delete=models.PROTECT)
    forma_pago = models.ForeignKey(FormaPago, db_column="fpn_forma_pago", on_delete=models.PROTECT)
    plazo = models.IntegerField(db_column="fpn_plazo", null=True, blank=True, verbose_name = "Plazo")
    valor = models.FloatField(db_column="fpn_valor", null=True, blank=True, verbose_name="Valor")
    usuario = models.ForeignKey(User, db_column="fpn_usuario", on_delete= models.PROTECT)
    
    def __str__(self):
        return str(self.id)
    
    
    class Meta:
        verbose_name = "Forma de pago Nota de Debito"
        verbose_name_plural = "Formas de pago Nota de Debito"
        
    def search(id=int):
        try:
            return FormaPagoNotaDebito.objects.filter(id=id)
        except BaseException as ex:
            return ex
    
    def search_to_nota_debito(id=int):
        try:
            return FormaPagoNotaDebito.objects.filter(nota_debito=id)
        except BaseException as ex:
            return ex
    
    def remove(id = int):
        try:
            FormaPagoNotaDebito.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex
    def update(formaPagoDebito):
        try:
            FormaPagoNotaDebito.objects.filter(id=formaPagoDebito.id).update(
                nota_debito= formaPagoDebito.nota_debito,
                forma_pago= formaPagoDebito.forma_pago,
                plazo= formaPagoDebito.plazo,
                valor= formaPagoDebito.valor,
                usuario= formaPagoDebito.usuario,
            )
            return True
        except BaseException as ex:
            return ex
        
    
        
        
    
    
    

class NotaCredito(models.Model):
    COMPROBANTES = (
        ("01", "Factura"),
    )
    ESTADOS = (("1", "Emitido"),
               ("2", "Anulado"))

    id = models.AutoField(db_column="ncr_id", primary_key=True)
    establecimiento = models.ForeignKey(
        Establecimiento, db_column="ncr_est", on_delete=models.CASCADE, verbose_name="Establecimiento")
    puntoEmision = models.ForeignKey(
        PuntoEmision, db_column="ncr_p_emision", on_delete=models.CASCADE, verbose_name="Punto de emisión")
    secuencia = models.IntegerField(
        db_column="ncr_secuencia", null=False, blank=False, verbose_name="Secuencia")
    autorizacion = models.CharField(
        db_column="ncr_autorizacion", max_length=49, null=False, blank=False, verbose_name="Autorización")
    claveacceso = models.CharField(
        db_column="ncr_claveacceso", max_length=49, null=False, blank=False, verbose_name="Clave de acceso")
    fecha = models.DateField(db_column="ncr_fecha",
                             null=False, blank=False, verbose_name="Fecha")
    comprobanteModificado = models.CharField(
        db_column="ncr_comp_mod", max_length=20, null=False, blank=False, choices=COMPROBANTES, verbose_name="Comprobante modificado")
    establecimientoDoc = models.CharField(
        db_column="ncr_comp_est_doc", max_length=3, null=False, blank=False, verbose_name="Establecimiento comprobante")
    puntoEmisionDoc = models.CharField(db_column="ncr_p_emi_doc", max_length=3,
                                       null=False, blank=False, verbose_name="Punto de emisión comprobante")
    secuenciaDoc = models.CharField(db_column="ncr_secuencia_doc", max_length=9,
                                    null=False, blank=False, verbose_name="Secuencia comprobante")
    motivo = models.CharField(
        db_column="ncr_motivo", max_length=250, null=True, blank=True, verbose_name="Motivo")
    tarifa0 = models.FloatField(
        db_column="ncr_tarifa0", null=False, blank=False, default=0.00, verbose_name="Tarifa 0%")
    tarifadif0 = models.FloatField(db_column="ncr_tarifadif0", null=False,
                                   blank=False, default=0.00, verbose_name="Tarifa diferente 0%")
    noObjetoIva = models.FloatField(
        db_column="ncr_noobjetoiva", null=False, blank=False, default=0.00, verbose_name="No objeto de IVA")
    descuento = models.FloatField(
        db_column="ncr_descuento", null=False, blank=False, default=0.00, verbose_name="Descuento")
    excento = models.FloatField(
        db_column="ncr_excento", null=False, blank=False, default=0.00, verbose_name="Excento")
    valorIce = models.FloatField(
        db_column="ncr_valor_ice", null=False, blank=False, default=0.00, verbose_name="Valor ICE")
    valorirbpnr = models.FloatField(
        db_column="ncr_valor_ibpnr", null=False, blank=False, default=0.00, verbose_name="Valor irbpnr")
    iva = models.FloatField(db_column="ncr_iva", null=False,
                            blank=False, default=0.00, verbose_name="IVA")
    total = models.FloatField(db_column="ncr_total", null=False,
                              blank=False, default=0.00, verbose_name="Total")
    estado = models.CharField(db_column="ncr_estado", max_length=5, null=False,
                              blank=False, default="1", choices=ESTADOS, verbose_name="Estado")
    emisor = models.ForeignKey(
        Emisor, db_column="ncr_emisor", on_delete=models.PROTECT, verbose_name="Emisor")
    usuario = models.ForeignKey(
        User, db_column="ncr_usuario", on_delete=models.PROTECT, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Nota de crédito"
        verbose_name_plural = "Notas de crédito"

    def create(nota_credito):
        nc = None
        try:
            nc = NotaCredito.objects.filter(_establecimiento=nota_credito.establecimiento,
                                            _puntoEmision=nota_credito.puntoEmision, _secuencia=nota_credito.secuencia, _emisor=nota_credito.emisor)
            if nc == None:
                nota_credito.save()
                return nota_credito._id
            else:
                return None
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return NotaCredito.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def search_to_serie(emisor_id=int, establecimiento=str, p_emision=str, secuencia=str):
        try:
            est = Establecimiento.objects.get(serie=establecimiento)
            p_emi = PuntoEmision.objects.get(
                serie=p_emision, establecimiento=est.id)
            return NotaCredito.objects.filter(establecimiento=est.id, puntoEmision=p_emi._id, emisor=emisor_id, secuencia=secuencia)
        except BaseException as ex:
            return ex
        
    def remove(id=int):
        try:
            NotaCredito.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def update(nota_credito):
        try:
            NotaCredito.objects.filter(id=nota_credito.id).update(
                establecimiento=nota_credito.establecimiento,
                puntoEmision=nota_credito.puntoEmision,
                secuencia=nota_credito.secuencia,
                autorizacion=nota_credito.autorizacion,
                claveacceso=nota_credito.claveacceso,
                fecha=nota_credito.fecha,
                comprobanteModificado=nota_credito.comprobanteModificado,
                establecimientoDoc=nota_credito.establecimientoDoc,
                puntoEmisionDoc=nota_credito.puntoEmisionDoc,
                secuenciaDoc=nota_credito.secuenciaDoc,
                motivo=nota_credito.motivo,
                tarifa0=nota_credito.tarifa0,
                tarifadif0=nota_credito.tarifadif0,
                noObjetoIva=nota_credito.noObjetoIva,
                descuento=nota_credito.descuento,
                excento=nota_credito.excento,
                valorIce=nota_credito.valorIce,
                valorirbpnr=nota_credito.valorirbpnr,
                iva=nota_credito.iva,
                total=nota_credito.total,
                estado=nota_credito.estado,
                emisor=nota_credito.emisor,
                usuario=nota_credito.usuario)
        except BaseException as ex:
            return ex

    def list_to_emisor_range(emisor_id, start, end):
        try:
            return NotaCredito.objects.filter(emisor=emisor_id, fecha__range=[start, end])
        except BaseException as ex:
            return ex


class OtroNDNC(models.Model):
    id = models.AutoField(
        db_column="odc_id", primary_key=True, verbose_name="Id")
    nombre = models.CharField(db_column="odc_nombre", max_length=255,
                              null=False, blank=False, default="sn", verbose_name="Nombre")
    descripcion = models.CharField(db_column="odc_descripcion", max_length=255,
                                   null=True, blank=True, default="", verbose_name="Descripcion")
    notaDebito = models.ForeignKey(
        NotaDebito, db_column="odc_nota_debito", on_delete=models.CASCADE, verbose_name="Nota de debito")
    notaCredito = models.ForeignKey(
        NotaCredito, db_column="odc_nota_credit", on_delete=models.CASCADE, verbose_name="Nota de crédito")
    usuario = models.ForeignKey(
        User, db_column="odc_usuario", on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Nota de crédito"
        verbose_name_plural = "Notas de crédito"

    def create(otronc):
        try:
            otronc.save()
            return otronc.id
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return OtroNDNC.objects.get(id=id)
        except BaseException as ex:
            return ex

    def update(otronc):
        try:
            return OtroNDNC.objects.filter(id=otronc.id).update(nombre=otronc.nombre, descripcion=otronc.descripcion, notaDebito=otronc.notaDebito, notaCredito=otronc.notaCredito, usuario=otronc.usuario)
        except BaseException as ex:
            return ex

    def list_to_nd(nota_debito_id=int):
        try:
            return OtroNDNC.objects.filter(notaDebito=nota_debito_id)
        except BaseException as ex:
            return ex

    def list_to_nc(nota_credito_id=int):
        try:
            return OtroNDNC.objects.filter(notaCredito=nota_credito_id)
        except BaseException as ex:
            return ex
        
    def remove(id = int):
        try:
            OtroNDNC.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex


class DetalleNC(models.Model):
    id = models.AutoField(
        db_column="dnc_id", primary_key=True, verbose_name="Id")
    cantidad = models.FloatField(
        db_column="dnc_cantidad", null=False, blank=False, default=0.00, verbose_name="Cantidad")
    valorUnitario = models.FloatField(
        db_column="dnc_valor_unitario", null=False, blank=False, default=0.00, verbose_name="Valor Unitario")
    descuento = models.FloatField(
        db_column="dnc_descuento", null=False, blank=False, default=0.00, verbose_name="Descuento")
    ice = models.FloatField(
        db_column="dnc_ice", null=False, blank=False, default=0.00, verbose_name="ICE")
    valorTotal = models.FloatField(
        db_column="dnc_valor_total", null=False, blank=False, default=0.00, verbose_name="Valor total")
    irbpnr = models.FloatField(
        db_column="dnc_irbpnr", null=False, blank=False, default=0.00, verbose_name="IRBPNR")
    notaCredito = models.ForeignKey(
        NotaCredito, db_column="dnc_nota_credito", on_delete=models.CASCADE, verbose_name="Nota de crédito")
    producto = models.ForeignKey(
        Producto, db_column="dnc_producto", on_delete=models.CASCADE, verbose_name="Producto")
    usuario = models.ForeignKey(
        User, db_column="dnc_usuario", on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Detalle nota de crédito"
        verbose_name_plural = "Detalles Nota de crédito"

    def create(detalle_nc):
        try:
            detalle_nc.save()
            return detalle_nc.id
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return DetalleNC.objects.get(id=id)
        except BaseException as ex:
            return ex

    def remove(id=int):
        try:
            DetalleNC.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def update(detalle_nc):
        try:
            DetalleNC.objects.filter(id=detalle_nc.id).update(cantidad=detalle_nc.cantidad, valorUnitario=detalle_nc.valorUnitario, descuento=detalle_nc.descuento, ice=detalle_nc.ice,
                                                               valorTotal=detalle_nc.valorUnitario, irbpnr=detalle_nc.irbpnr, notaCredito=detalle_nc.notaCredito, producto=detalle_nc.producto, usuario=detalle_nc.usuario)
            return True
        except BaseException as ex:
            return ex

    def list_to_nc(nc_id=int):
        try:
            return DetalleNC.objects.filter(_notaCredito=nc_id)
        except BaseException as ex:
            return ex


class RetencionCodigo(models.Model):
    id = models.AutoField(
        db_column="rco_id", primary_key=True, verbose_name="Id")
    codigo = models.CharField(
        db_column="rco_codigo", max_length=20, null=False, blank=False, verbose_name="Código")
    porcentaje = models.FloatField(
        db_column="rco_porcentaje", null=False, blank=False, verbose_name="Porcentaje")
    detalle = models.CharField(db_column="rco_detalle", max_length=255,
                               null=False, blank=False, default="sn", verbose_name="Detalle")
    tipo = models.CharField(db_column="rco_tipo", max_length=20,
                            null=False, blank=False, verbose_name="Tipo")
    usuario = models.ForeignKey(User,
                                db_column="rco_usuario", on_delete=models.PROTECT, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Código de retención"
        verbose_name_plural = "Códigos de retenciones"

    def create(retencion_codigo):
        try:
            retencion_codigo.save()
            return retencion_codigo.id
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return RetencionCodigo.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def search_to_codigo(codigo=str):
        try:
            return RetencionCodigo.objects.filter(codigo=codigo)
        except BaseException as ex:
            return ex

    def remove(id=int):
        try:
            RetencionCodigo.objects.filter(id=id).delete()
        except BaseException as ex:
            return ex

    def update(retencion_codigo):
        try:
            RetencionCodigo.objects.filter(id=retencion_codigo.id).update(codigo=retencion_codigo.codigo, porcentaje=retencion_codigo.porcentaje,
                                                                          detalle=retencion_codigo.detalle, tipo=retencion_codigo.tipo, usuario=retencion_codigo.usuario)
            return True
        except BaseException as ex:
            return ex

    def list_all():
        try:
            return RetencionCodigo.objects.all()
        except BaseException as ex:
            return ex


class Retencion(models.Model):

    TYPE_DOCUMENTO = (("01", "01:Factura"),)

    id = models.AutoField(
        db_column="ret_id", primary_key=True, verbose_name="Id")
    emisor = models.ForeignKey(
        Emisor, db_column="ret_emisor", on_delete=models.PROTECT, verbose_name="Emisor")
    sujeto_retenido = models.ForeignKey(
        Cliente, db_column="ret_sujeto", on_delete=models.PROTECT, verbose_name="Retenido")
    establecimiento = models.ForeignKey(
        Establecimiento, db_column="ret_establecimiento", on_delete=models.PROTECT, verbose_name="Establecimiento")
    pemision = models.ForeignKey(PuntoEmision, db_column="ret_pemision",
                                 on_delete=models.PROTECT, verbose_name="Punto de emisión")
    secuencia = models.CharField(
        db_column="ret_secuencia", max_length=9, null=False, blank=False, verbose_name="Secuencia")
    fecha = models.DateField(db_column="ret_fecha",
                             null=False, blank=False, verbose_name="Fecha")
    tipo_documento = models.CharField(db_column="ret_tipo_doc", max_length=50,
                                      null=False, blank=False, choices=TYPE_DOCUMENTO, verbose_name="Tipo de documento")
    estab_doc = models.CharField(db_column="ret_estab_doc", max_length=3,
                                 null=False, blank=False, verbose_name="Estab de documento")
    pemis_doc = models.CharField(db_column="ret_pemis", max_length=3,
                                 null=False, blank=False, verbose_name="Punto de emisión de documento")
    secuencia_doc = models.CharField(
        db_column="ret_secuencia_doc", max_length=9, null=False, blank=False, verbose_name="Secuencia documento")
    autorizacion = models.CharField(
        db_column="ret_autorizacion", max_length=49, null=True, blank=False, verbose_name="Autorización")
    clave_acceso = models.CharField(
        db_column="ret_clave_acceso", max_length=49, null=False, blank=False, verbose_name="Clave de acceso")
    usuario = models.ForeignKey(
        User, db_column="ret_usuario", on_delete=models.PROTECT, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Retención"
        verbose_name_plural = "Retenciones"

    def create(retencion):
        try:
            retencion.save()
            return retencion.id
        except BaseException as ex:
            return ex

    def update(retencion):
        try:
            Retencion.objects.filter(id=retencion.id).update(emisor=retencion.emisor, sujeto_retenido=retencion.sujeto_retenido, establecimiento=retencion.establecimiento, pemision=retencion.pemsision, secuencia=retencion.secuencia, fecha=retencion.fecha,
                                                             tipo_documento=retencion.tipo_documento, estab_doc=retencion._estab_doc, pemis_doc=retencion.pemis_doc, secuencia_doc=retencion.secuencia, autorizacion=retencion.autorizacion, clave_acceso=retencion.clave_acceso, usuario=retencion.usuario)
            return True
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return Retencion.objects.get(id=id)
        except BaseException as ex:
            return ex

    def search_to_secuencia(emisor_id=int, establecimiento=str, p_emision=str, secuencia=str):
        try:
            est = Establecimiento.objects.get(serie=establecimiento)
            pemi = None
            for pem in PuntoEmision.objects.filter(serie=p_emision, establecimiento=est.id):
                pemi = pem
            return Retencion.objects.filter(emisor=emisor_id, establecimiento=est, pemision=pemi, secuencia=secuencia)
        except BaseException as e:
            return e

    def remove(id=int):
        try:
            Retencion.objects.filter(id=id).delete()
        except BaseException as ex:
            return ex

    def list_to_emisor_range(emisor_id=int, start=str, end=str):
        try:
            return Retencion.objects.filter(emisor=emisor_id, fecha__range=[start, end])
        except BaseException as ex:
            return ex


class RetencionCompra(models.Model):
    id = models.AutoField(
        db_column="rcp_id", primary_key=True, verbose_name="Id")
    baseImponible = models.FloatField(
        db_column="rcp_base_imp", null=False, blank=False, default=0.00, verbose_name="Base imponible")
    valor_retenido = models.FloatField(
        db_column="rcp_valor_retenido", null=False, blank=False, default=0.00, verbose_name="Valor retenido")
    retencion = models.ForeignKey(
        Retencion, db_column="rcp_retencion", on_delete=models.PROTECT, verbose_name="Retención")
    retencion_codigo = models.ForeignKey(
        RetencionCodigo, db_column="rcp_retencion_codigo", on_delete=models.PROTECT, verbose_name="Código de retención")
    emisor = models.ForeignKey(
        Emisor, db_column="rcp_emisor", on_delete=models.PROTECT, verbose_name="Emisor")
    usuario = models.ForeignKey(
        User, db_column="rcp_usuario", on_delete=models.PROTECT, verbose_name="Usuario")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Retención compra"
        verbose_name_plural = "Retenciones compras"

    def create(retencion_compra):
        try:
            retencion_compra.save()
            return retencion_compra.id
        except BaseException as ex:
            return ex

    def update(retencion_compra):
        try:
            RetencionCompra.objects.filter(id=retencion_compra.id).update(
                baseImponible=retencion_compra.baseImponible, valor_retenido=retencion_compra.valor_retenido, retencion=retencion_compra.retencion, emisor=retencion_compra.emisor, usuario=retencion_compra.usuario
            )
            return True
        except BaseException as ex:
            return ex

    def search(id=int):
        try:
            return RetencionCompra.objects.filter(id=id)
        except BaseException as ex:
            return ex

    def search_to_retencion(retencion_id=int):
        try:
            return RetencionCompra.objects.filter(retencion=retencion_id)
        except BaseException as ex:
            return ex

    def search_to_codigo(codigo_id=int):
        try:
            return RetencionCompra.objects.filter(retencion_codigo=codigo_id)
        except BaseException as ex:
            return ex

    def remove(id=int):
        try:
            RetencionCompra.objects.filter(id=id).delete()
            return True
        except BaseException as ex:
            return ex

    def list_to_emisor(emisor_id=int):
        try:
            return RetencionCompra.objects.filter(emisor=emisor_id)
        except BaseException as ex:
            return ex
