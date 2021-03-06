from ast import Is
from asyncio.log import logger
import datetime
from distutils.log import error
import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from facturacion.serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework import status, viewsets
from django.db import transaction, IntegrityError

from ventas.forms import UserForm
from ventas.models import *


def views_index(request):
    return render(request, "ventas/home/index.html")

#################API REST ######################


class ChangePasswordView(UpdateAPIView):
    """
        An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }


class SessionExpiredMiddleware:
    def process_request(request):
        last_activity = request.session['last_activity']
        now = datetime.now()

        if (now - last_activity).minutes > 10:
            # Do logout / expire session
            # and then...
            return Response({"code": "401", "sms": "Sessi??n expirada"})

        if not request.is_ajax():
            # don't set this for ajax requests or else your
            # expired session checks will keep the session from
            # expiring :)
            request.session['last_activity'] = now


class RegisterUsers(APIView):
    """Clase para usuarios para registrar un nuevo usuario.
    """

    def post(self, request, format=None):
        register = UserForm(data=request.data)

        if register.is_valid():
            user = register.save()
            pw = user.password
            user.set_password(pw)
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


"""
class UserViewSet(viewsets.GenericViewSet):
    
    queryset = User.objects.filter(is_active=True)
    serilizer_class = UserModelSerializer
    
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'acces_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)
"""


class Login(ObtainAuthToken):
    """Clase api, para realizar un login.
    """

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        username = User.objects.get(email=email)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'pk': user.pk,
                'user': user.username,
            })


class Logout(APIView):
    '''Clase api, para elimina el token y cerrar session.
    '''

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class EmisorView(LoginRequiredMixin, APIView):
    """API para obtener todos los emisores, y registrar un nuevo emisor.
    """
    # Valida que este autentificado
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="GET")
    def get(self, request, format=None, *args, **kwargs):
        # Para obtener todos los emisores.
        if request.user.is_authenticated:
            emisor = Emisor.objects.all()
            serializer = EmisorSerializer(emisor, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="POST")
    def post(self, request, format=None):
        # Para registrar un nuevo emisor.
        if request.user.is_authenticated:
            serializer = EmisorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class EmisorUpdate(LoginRequiredMixin, APIView):
    """Api para actualizar un emisor
    """
    @action(detail=False, method="POST")
    def post(self, request, format=json):
        if request.user.is_authenticated:
            serializer = EmisorSerializer(data=request.data)
            #print("update ", serializer)
            if serializer.is_valid:
                emisor = Emisor(id=request.data["id"],
                                identificacion=request.data["identificacion"],
                                tipo_id=request.data["tipo_id"],
                                rasonSocial=request.data["rasonSocial"],
                                nombreComercial=request.data["nombreComercial"],
                                telefono=request.data["telefono"],
                                direccionMatriz=request.data["direccionMatriz"],
                                contribuyenteEspecial=request.data["contribuyenteEspecial"],
                                obligadoLlevarContabilidad=request.data["obligadoLlevarContabilidad"],
                                regimenMicroempresa=request.data["regimenMicroempresa"],
                                agenteRetencion=request.data["agenteRetencion"],
                                logo=request.data["logo"],
                                ambiente=request.data["ambiente"],
                                tipoToken=request.data["tipoToken"],
                                firma=request.data["firma"],
                                estado=request.data["estado"],
                                cantidad_usuario=request.data["cantidad_usuario"],
                                usuario=request.user)
                res = Emisor.actualizarEmisor(emisor)
                if res != True:
                    return Response({"sms": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    print("res ", res)
                    return Response(status=status.HTTP_201_CREATED)
            else:
                print("error ")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class EmisorGetIdentificacion(LoginRequiredMixin, APIView):
    """
    Api para obenter un emisor, por su numero de identificacion.
    """

    def get(self, request, format=None, *args, identificacion):
        if request.user.is_authenticated:
            emisor = Emisor.buscarEmisor(identificacion)
            serializer = EmisorSerializer(emisor, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class EmisorDisable(LoginRequiredMixin, APIView):
    """Api para actualizar un emisor
    """
    @action(detail=False, method="POST")
    def get(self, request, format=None, *args, pk):
        if request.user.is_authenticated:
            for emisor in Emisor.buscarEmisor_id(pk):
                emisor.estado = 2
                res = Emisor.actualizarEmisor(emisor)
                if res != True:
                    return Response({"sms": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    print("res ", res)
                    return Response(status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class EmisorGetId(ListAPIView):
    """
    Api para obtener un emisor, por su id.
    """
    serializer_class = EmisorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="GET")
    def get_queryset(self):
        if self.request.user.is_authenticated:
            id = self.kwargs["id"]
            try:
                return Emisor.search_id(id)
            except BaseException as ex:
                return Response({"Error: ": str(ex)}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class EstablecimientoCreate(LoginRequiredMixin, APIView):
    """
    API para crud un establecimiento
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):
        try:
            if request.user.is_authenticated:
                serializer = EstablecimientoSerializer(data=request.data)
                puntos_emision = request.data.pop("puntos_emision")
                if serializer.is_valid():
                    print("emisor id ", request.data["emisor"])
                    emisor_temp = Emisor.objects.get(
                        id=int(request.data["emisor"]))
                    establecimiento = Establecimiento(
                        serie=request.data["serie"],
                        nombre=request.data["nombre"],
                        telefono=request.data["telefono"],
                        direccion=request.data["direccion"],
                        emisor=emisor_temp,
                        usuario=request.user
                    )
                    res = Establecimiento.create(establecimiento)
                    print("res ", res)
                    if type(res) == str:
                        return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        puntos = []
                        for punto_emision in puntos_emision:
                            pemis_temp = PuntoEmision(serie=punto_emision["serie"],
                                                      descripcion=punto_emision["descripcion"],
                                                      establecimiento=Establecimiento(
                                                          id=res.id),
                                                      estado=punto_emision["estado"],
                                                      usuario=request.user)
                            res_pemi = PuntoEmision.create(pemis_temp)
                            if type(res_pemi) != str:
                                puntos.append(res_pemi.id)
                            print(res_pemi)
                        serializers = EstablecimientoSerializer(
                            Establecimiento.objects.filter(id=res.id), many=True)
                        return Response(serializers.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("error ", e)
            return Response({"Error: "+str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):
        """Metodo para actualizar el establecimiento.
        """
        if request.user.is_authenticated:
            serializer = EmisorSerializer(data=request.data)
            if serializer.is_valid:
                emisor_temp = None
                for emisor in Emisor.search_id(request.data["emisor"]):
                    emisor_temp = emisor

                establecimiento = Establecimiento(id=request.data["id"],
                                                  serie=request.data["serie"],
                                                  nombre=request.data["nombre"],
                                                  telefono=request.data["telefono"],
                                                  direccion=request.data["direccion"],
                                                  emisor=emisor_temp,
                                                  usuario=request.user)
                res = Establecimiento.update(establecimiento)
                if res == True:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"error: ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="GET")
    def get(self, request, format=None, *args, pk):
        """
        Metodo para obtener los establecimientos de un emisor o facturador.
        """
        if request.user.is_authenticated:
            establecimientos = Establecimiento.list_to_emisor(pk)
            serializer = EstablecimientoSerializer(establecimientos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="DELETE")
    def delete(self, request, format=None, *args, pk):
        """
        Metodo para eliminar un establecimiento
        """
        print("enntro delete")
        if request.user.is_authenticated:
            res = Establecimiento.remove(pk)
            if res == True:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class PuntoEmisionViews(LoginRequiredMixin, APIView):
    """
    API para crud de los puntos de emision.
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=None):
        if request.user.is_authenticated:
            serializers = PuntoEmisionSerializer(data=request.data)
            if serializers.is_valid():
                pemi = PuntoEmision(serie=request.data["serie"],
                                    descripcion=request.data["descripcion"],
                                    establecimiento=Establecimiento(
                                        id=int(request.data["establecimiento"])),
                                    estado=request.data["estado"],
                                    usuario=request.user
                                    )

                res = PuntoEmision.create(pemi)
                if type(res) != str:
                    serializer = PuntoEmisionSerializer(
                        PuntoEmision.objects.filter(id=res.id), many=True)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"Error: ": str(res)}, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="PUT")
    def put(self, request, format=None):
        """
        Metodo para actualizar un punto de emision.
        """
        if request.user.is_authenticated:
            try:
                establecimiento = Establecimiento.objects.get(
                    id=request.data["establecimiento"])

                punto_emision = PuntoEmision(id=request.data["id"],
                                             serie=request.data["serie"],
                                             descripcion=request.data["descripcion"],
                                             establecimiento=establecimiento,
                                             estado=request.data["estado"],
                                             usuario=request.user)
                res = PuntoEmision.update(punto_emision)
                if res == True:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error: ": str(res)}, status=status.HTTP_204_NO_CONTENT)
            except BaseException as ex:
                return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="GET")
    def get(self, request, format=None, *args, id_puntoemision):
        """ Metodo para obtener un punto de emision por su id.
        """
        if request.user.is_authenticated:
            try:
                puntos_emision = PuntoEmision.search_id(id_puntoemision)
                serializer = PuntoEmisionSerializer(puntos_emision, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"Error: ": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="DELETE")
    def delete(self, request, format=None, *args, id_puntoemision):
        """ 
        Metodo para eliminar un punto de emision por su id.
        """
        try:
            if request.user.is_authenticated:
                res = PuntoEmision.remove(id_puntoemision)
                if res == True:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"Error: ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({"Error: ": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PuntoEmisionList(ListAPIView):

    serializer_class = PuntoEmisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Metodo para listar los puntos de emision de un establecimiento.
        """
        establecimiento_id = self.kwargs['estblecimiento_id']
        if self.request.user.is_authenticated:
            try:
                return PuntoEmision.list_to_establecimiento(establecimiento_id)
            except BaseException as e:
                return Response({"Error: ": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ClienteViews(LoginRequiredMixin, APIView):
    """
    API para crud de cliente
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=None):
        if request.user.is_authenticated:
            try:
                serializers = ClienteSerializer(data=request.data)
                if serializers.is_valid():
                    cli_temp = Cliente.objects.filter(
                        identificacion=request.data["identificacion"], emisor=Emisor(id=request.data["emisor"]))
                    if len(cli_temp) <= 0:
                        serializers.save()
                        return Response(serializers.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"Error: ": "El cliente ya se encuentra registrado."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializers.errors ,status=status.HTTP_400_BAD_REQUEST)
            except BaseException as ex:
                return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):
        """
        Metodo para actualizar los datos de un cliente de un emisor. 
        """
        if request.user.is_authenticated:
            try:
                emisor_tmp = Emisor.objects.get(id=request.data["emisor"])
                cliente = Cliente(
                    id=request.data["id"],
                    nombreApellido=request.data['nombreApellido'],
                    identificacion=request.data['identificacion'],
                    tipoIdentificacion=request.data['tipoIdentificacion'],
                    direccion=request.data['direccion'],
                    telefono=request.data['telefono'],
                    extension=request.data['extension'],
                    movil=request.data['movil'],
                    mail=request.data['mail'],
                    usuario=request.user,
                    emisor=emisor_tmp
                )
                res = Cliente.update(cliente)
                if res == True:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except BaseException as ex:
                return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                cliente = Cliente.search(pk)
                serializer = ClienteSerializer(cliente, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({"Error: ": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = Cliente.remove(pk)
                if res == True:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"Error: ": str(res)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListClienteToEmisor(ListAPIView):
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Metodo para listar los clientes de un emisor.
        """
        try:
            emisor_id = self.kwargs["pk"]
            if self.request.user.is_authenticated:
                return Cliente.list(emisor_id)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as e:
            return Response({"Error: ": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Web service producto
class ProductoViews(LoginRequiredMixin, APIView):
    """API para crud de producto
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):
        try:
            if request.user.is_authenticated:
                serializer = ProductoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.create()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except BaseException as ex:
            return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):
        try:
            if request.user.is_authenticated:
                serializer = ProductoSerializer(data=request.data)
                if serializer.is_valid:
                    producto = Producto(id=request.data["id"],
                                        nombre=request.data["nombre"],
                                        codigoPrincipal=request.data["codigoPrincipal"],
                                        codigoAuxiliar=request.data["codigoAuxiliar"],
                                        tipo=request.data["tipo"],
                                        ice=request.data["ice"],
                                        irbpnr=request.data["irbpnr"],
                                        precio1=request.data["precio1"],
                                        precio2=request.data["precio2"],
                                        precio3=request.data["precio3"],
                                        precio4=request.data["precio4"],
                                        tipo_iva=Iva(
                                            id=request.data["tipo_iva"]),
                                        valor_iva=request.data["valor_iva"],
                                        descripcion=request.data["descripcion"],
                                        emisor=Emisor(
                                            id=request.data["emisor"]),
                                        usuario=request.user)
                    res = Producto.update(producto)

                    if res == True:
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response({"Error: ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BaseException as ex:
            return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):

        if request.user.is_authenticated:
            id_pro = pk
            res = Producto.search(id_pro)
            serializer = ProductoSerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        if request.user.is_authenticated:
            id_pro = pk
            res = Producto.remove(id_pro)
            if res == True:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"Error: ": str(res)}, status=status.HTTP_200_OK)


class ProductoListEmisor(ListAPIView):
    """
    API para listar los productos de un emisor.
    """
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_authenticated:
            emisor_id = self.kwargs['emisor_id']
            try:
                return Producto.list_to_emisor(emisor_id)
            except BaseException as ex:
                return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class FacturaView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):
        try:
            with transaction.atomic():
                print("ingreso")
                if request.user.is_authenticated:
                    print('data factura_detalle ', len(
                        request.data["factura_detalle"]))
                    serializer = FacturaCabeceraSerializer(data=request.data)

                    #print("serializer ", serializer)

                    if serializer.is_valid():

                        facts = FacturaCabecera.search_to_factura(
                            request.data["establecimiento"], request.data["punto_emision"], request.data["secuencia"], request.data["emisor"])
                        
                        if len(facts) > 0:
                            return Response({"Error: ": "Ya existe una factura con estos datos."}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            
                            fecha = request.data["fecha"]
                            emi_temp = Emisor.objects.get(id=request.data["emisor"])
                            est_temp = Establecimiento.objects.get(id = request.data["establecimiento"])
                            pemi_temp = PuntoEmision.objects.get(id = request.data["punto_emision"])
                            
                            
                            #Para generar el codigo de acceso.
                            access_key = modulo11(
                                fecha, "01", str(emi_temp.identificacion),
                                str(emi_temp.ambiente), str(est_temp.serie), str(pemi_temp.serie),
                                (str(request.data["secuencia"])).zfill(9), "1")
                            
                            serializer.save(autorizacion=access_key, claveacceso=access_key)
                            print("factura guardada ")
                            
                            impuestos = request.data["impuestos_factura"]
                            for impuesto in impuestos:
                                imp_factura = ImpuestoFactura(
                                    base = impuesto["base"],
                                    valor = impuesto["valor"],
                                    iva = Iva(id=impuesto["iva"]),
                                    facturaCabecera = FacturaCabecera(id=serializer.data["id"]),
                                    usuario = request.user
                                )
                                imp_factura.save()
                                print("impuesto factura guardada")
                                logger.message("impuesto factura guardada")
                                

                            data_factura_detalle = request.data["factura_detalle"]
                            #tam_factura_detalle = len(data_factura_detalle)
                            for detail in data_factura_detalle:
                                tem_cantidad = detail["cantidad"]
                                tem_valor_unitario = detail["valorUnitario"]
                                tem_descuento = detail["descuento"]
                                tem_ice = detail["ice"]
                                tem_valor_total = detail["valorTotal"]
                                tem_irbpnr = detail["irbpnr"]
                                tem_factura = serializer.data["id"]
                                tem_producto = detail["producto"]
                                tem_usuario = request.user

                                factura_detalle = FacturaDetalle(
                                    cantidad=tem_cantidad,
                                    valorUnitario=tem_valor_unitario,
                                    descuento=tem_descuento,
                                    ice=tem_ice,
                                    valorTotal=tem_valor_total,
                                    irbpnr=tem_irbpnr,
                                    factura=FacturaCabecera(id=tem_factura),
                                    producto=Producto(id=tem_producto),
                                    usuario=tem_usuario,
                                )
                                res = FacturaDetalle.create(factura_detalle)
                                print("detalle guardado ", str(res))

                            data_forma_pagos_factura = request.data["forma_pago_factura"]
                            for pago in data_forma_pagos_factura:
                                temp_formaPago = pago["formaPago"]
                                temp_tiempo = pago["tiempo"]
                                temp_plazo = pago["plazo"]
                                temp_valor = pago["valor"]
                                temp_usuario = request.user

                                forma_pago_factura = FormaPagoFactura(
                                    formaPago=FormaPago(id=temp_formaPago),
                                    facturaid=FacturaCabecera(
                                        id=serializer.data["id"]),
                                    tiempo=temp_tiempo,
                                    plazo=temp_plazo,
                                    valor=temp_valor,
                                    usuario=temp_usuario
                                )

                                res = FormaPagoFactura.create(
                                    forma_pago_factura)
                                print("registrado forma de pago factura ", str(res))
                            #tam_forma_pagos_factura =  len(data_forma_pagos_factura)

                            data_otros_factura = request.data["otro_factura"]

                            for otro in data_otros_factura:
                                tem_nombre = otro["nombre"]
                                tem_descripcion = otro["descripcion"]
                                tem_factura = serializer.data["id"]

                                otro_factura = Otro(
                                    nombre=tem_nombre,
                                    descripcion=tem_descripcion,
                                    factura=FacturaCabecera(id=tem_factura)
                                )
                                res = Otro.create(otro_factura)
                                print("Registrado otro factura ", str(res))

                            #tam_otros_factura = len(data_otros_factura)

                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"Error": "Formato invalido. "}, status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status.HTTP_401_UNAUTHORIZED)
        except IntegrityError:
            return Response({"Error": "Error de integridad"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BaseException as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):

        try:
            if request.user.is_authenticated:
                serializer = FacturaCabeceraSerializer(data=request.data)
                if serializer.is_valid():
                    facts = FacturaCabecera.search_to_factura(
                        request.data["establecimiento"], request.data["punto_emision"], request.data["secuencia"], request.data["emisor"])
                    if len(facts) > 0:
                        cabecera_factura = FacturaCabecera(
                            id=request.data["id"],
                            establecimiento=request.data["establecimiento"],
                            punto_emision=request.data["punto_emision"],
                            secuencia=request.data["secuencia"],
                            autorizacion=request.data["autorizacion"],
                            claveacceso=request.data["claveacceso"],
                            fecha=request.data["fecha"],
                            emisor=Emisor(id=request.data["emisor"]),
                            cliente=Cliente(id=request.data["cliente"]),
                            establecimientoGuia=request.data["establecimientoGuia"],
                            puntoGuia=request.data["puntoGuia"],
                            secuenciaGuia=request.data["secuenciaGuia"],
                            noobjetoiva=request.data["noobjetoiva"],
                            tarifa0=request.data["tarifa0"],
                            tarifadif0=request.data["tarifadif0"],
                            excentoiva=request.data["excentoiva"],
                            totaldescuento=request.data["totaldescuento"],
                            totalice=request.data["totalice"],
                            totalirbpnt=request.data["totalirbpnt"],
                            tipo_iva=request.data["tipo_iva"],
                            valor_iva=request.data["valor_iva"],
                            valorIva=request.data["valorIva"],
                            propina=request.data["propina"],
                            total=request.data["total"],
                            estado=request.data["estado"],
                            usuario=request.user,
                        )
                        res = FacturaCabecera.update(cabecera_factura)
                        if res == True:
                            return Response(status=status.HTTP_200_OK)
                        else:
                            return Response({"Error": "No se ha podido actualizar "+str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({"Error: ": "No existe una factura con estos datos."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):

        try:
            if request.user.is_authenticated:
                id_fact = pk
                res = FacturaCabecera.search_to_id(id_fact)
                serializer = FacturaCabeceraSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = FacturaCabecera.remove(pk)
                if res == True:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error: ": str(res)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FacturaListEmisorRangeDate(ListAPIView):
    """
    API para generar un reporte de rango de fechas incial y final de un emisor.
    """
    serializer_class = FacturaCabeceraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                id_emisor = self.kwargs["id_emisor"]
                date_init = self.kwargs["date_init"]
                date_end = self.kwargs["date_end"]

                return FacturaCabecera.list_to_range_date(date_init, date_end, id_emisor)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error:": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FacturaListEmisorMonth(ListAPIView):
    """
    API para generar un reporte de facturas emitidas, por un rango de fecha de mes y anio, de un emisor.
    """
    serializer_class = FacturaCabeceraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                id_emisor = self.kwargs["id_emisor"]
                month = self.kwargs["month"]
                year = self.kwargs["year"]

                return FacturaCabecera.list_to_month_year(month, year, id_emisor)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FacturDetalleViews(LoginRequiredMixin, APIView):

    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):
        try:
            if request.user.is_authenticated:
                serializer = FacturaDetalleSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):

        if request.user.is_authenticated:
            serializer = FacturaCabeceraSerializer(data=request.data)
            detalle = FacturaDetalle(
                id=request.data["id"],
                cantidad=request.data["cantidad"],
                valorUnitario=request.data["valorUnitario"],
                descuento=request.data["descuento"],
                ice=request.data["ice"],
                valorTotal=request.data["valorTotal"],
                irbpnr=request.data["irbpnr"],
                factura=FacturaCabecera(id=request.data["factura"]),
                producto=Producto(id=request.data["producto"]),
                usuario=request.user
            )
            res = FacturaDetalle.update(detalle)
            if res == True:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"Error: ": str(res)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):
        if request.user.is_authenticated:
            res = FacturaDetalle.search(pk)
            serializer = FacturaDetalleSerializer(res, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, pk):
        if request.user.is_authenticated:
            res = FacturaDetalle.remove(pk)
            if res == True:
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"Error: ": str(res)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotaDebitoView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):
        if request.user.is_authenticated:
            serializer = NotaDebitoSerializer(data=request.data)
            try:
                with transaction.atomic():
                    if serializer.is_valid():
                        nota_debito = NotaDebito.objects.filter(
                            establecimiento=request.data["establecimiento"], puntoEmision=request.data["puntoEmision"], secuencia=request.data["secuencia"])
                        if len(nota_debito) > 0:
                            return Response({"Error": "Este documento ya esta registrado."}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            fecha = request.data["fecha"]
                            emi_temp = Emisor.objects.get(id=request.data["emisor"])
                            est_temp = Establecimiento.objects.get(id = request.data["establecimiento"])
                            pemi_temp = PuntoEmision.objects.get(id = request.data["puntoEmision"])
                            
                            
                            #Para generar el codigo de acceso.
                            access_key = modulo11(
                                fecha, "05", str(emi_temp.identificacion),
                                str(emi_temp.ambiente), str(est_temp.serie), str(pemi_temp.serie),
                                (str(request.data["secuencia"])).zfill(9), "1")
                            print("access_key ",access_key)
                            serializer.save(autorizacion=access_key, claveacceso=access_key)

                            pagos = []
                            for pago in request.data["forma_pago_debito"]:
                                fpagond = FormaPagoNotaDebito(
                                    nota_debito=NotaDebito(
                                        serializer.data["id"]),
                                    forma_pago=FormaPago(
                                        id=pago["forma_pago"]),
                                    plazo=pago["plazo"],
                                    valor=pago["valor"],
                                    usuario=request.user
                                )
                                fpagond.save()
                                pagos.append(fpagond)
                                print("Forma de pago guardada.")
                            serializer_pagos = FormaPagoSerializer(data=pagos)
                            serializer.data["forma_pago_debito"] = serializer_pagos
                            otros = []
                            for otro in request.data["odc_nota_debito"]:
                                nombre = otro["nombre"]
                                descripcion = otro["descripcion"]

                                otrondnc = OtroNDNC(
                                    nombre=nombre,
                                    descripcion=descripcion,
                                    notaDebito=NotaDebito(
                                        id=serializer.data["id"]),
                                    usuario=request.user
                                )
                                resp = OtroNDNC.create(otrondnc)
                                print("resp ", resp)

                                if type(resp) == int:
                                    otros.append(otro)
                                    print("otros guardado nota de debito")
                            serializer_otro = OtroNDNCSerializer(data=otros)
                            serializer.data["odc_nota_debito"] = serializer_otro

                            return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError as ex:
                return Response({}, status)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):
        if request.user.is_authenticated:
            try:
                serializer = NotaDebitoSerializer(data=request.data)
                if serializer.is_valid():
                    nota_debito = NotaDebito(
                        id=request.data["id"],
                        establecimiento=Establecimiento(
                            id=request.data["establecimiento"]),
                        puntoEmision=PuntoEmision(
                            id=request.data["puntoEmision"]),
                        secuencia=request.data["secuencia"],
                        autorizacion=request.data["autorizacion"],
                        claveacceso=request.data["claveacceso"],
                        fecha=request.data["fecha"],
                        comprobanteModificado=request.data["comprobanteModificado"],
                        establecimientoDoc=request.data["establecimientoDoc"],
                        puntoEmisionDoc=request.data["puntoEmisionDoc"],
                        secuenciaDoc=request.data["secuenciaDoc"],
                        tarifa0=request.data["tarifa0"],
                        tarifadif0=request.data["tarifadif0"],
                        noObjetoIva=request.data["noObjetoIva"],
                        excento=request.data["excento"],
                        valorIce=request.data["valorIce"],
                        iva=request.data["iva"],
                        total=request.data["total"],
                        estado=request.data["estado"],
                        emisor=Emisor(id=request.data["emisor"]),
                        cliente=Cliente(id=request.data["cliente"]),
                        usuario=request.user
                    )
                    res = NotaDebito.update(nota_debito)
                    if res == True:
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response({"Error: ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except BaseException as ex:
                return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):
        if request.user.is_authenticated:
            try:
                nota_debito = NotaDebito.search_id(pk)
                serializer = NotaDebitoSerializer(nota_debito, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BaseException as ex:
                return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        if request.user.is_authenticated:
            try:
                res = NotaDebito.remove(pk)
                if res == True:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error: ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except BaseException as ex:
                return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListNotaDebitoEmisorRange(ListAPIView):
    """
    API Para listar las notas de debito en un rango de fechas de un emisor.
    """

    serializer_class = NotaDebitoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            id_emisor = self.kwargs["id_emisor"]
            start = self.kwargs["start"]
            end = self.kwargs["end"]

            return NotaDebito.list_to_emisor(id_emisor, start, end)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class OtroViews(LoginRequiredMixin, APIView):
    """
    API para post, put, get de otros de una factura.
    """

    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):

        if request.user.is_authenticated:
            serializer = OtroSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):

        if request.user.is_authenticated:
            serializer = OtroSerializer(data=request.data)
            if serializer.is_valid():

                otros = Otro.search(int(request.data["id"]))
                if len(otros) > 0:
                    id = request.data["id"]
                    otro = Otro(
                        id=id,
                        nombre=request.data["nombre"],
                        descripcion=request.data["descripcion"],
                        factura=FacturaCabecera(id=request.data["factura"])
                    )
                    res = Otro.update(otro)
                    if res == True:
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response({"Error": "Se ha generado un error "+str(res)}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"Error": "No se ha encontrado el item"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Error": "Los datos recibidos no son correctos"}, staus=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Acceso no autorizado"}, stutus=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):
        if request.user.is_authenticated:
            try:
                otro_id = pk
                res = Otro.search(otro_id)
                serializer = OtroSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BaseException as ex:
                return Response({"Error: ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Error": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        try:
            if Otro.remove(pk):
                return Response({"sms": "Item eliminado"}, status=status.HTTP_200_OK)
        except BaseException as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListToFacturaOtros(ListAPIView):
    """
    API para listar los items de otros de una factura.
    """
    serializer_class = OtroSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                id_factura = self.kwargs["id_factura"]

                return Otro.list_to_factura(id_factura)
            else:
                return Response({"Error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FormaPagoView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):
        try:
            if request.user.is_authenticated:
                serializer = FormaPagoSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Error": "El formato recibido no es valido "}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Error": "Acceso no autorizado"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BaseException as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, format=json):
        try:
            if request.user.is_authenticated:
                forma_pago_id = request.data["id"]
                if len(FormaPago.search(forma_pago_id)) > 0:
                    serializer = FormaPagoSerializer(data=request.data)
                    if serializer.is_valid:
                        forma_pago = FormaPago(
                            id=request.data["id"],
                            codigo=request.data["codigo"],
                            descripcion=request.data["descripcion"],
                            usuario=request.user
                        )
                        if FormaPago.update(forma_pago):
                            return Response({"sms": "F"}, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Acceso no autorizado"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except BaseException as ex:
            return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):
        if request.user.is_authenticated:
            try:
                forma_pago_id = pk
                res = FormaPago.search(forma_pago_id)
                serializer = FormaPagoSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except BaseException as ex:
                return Response({"Error": ex}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        if request.user.is_authenticated:
            res = FormaPago.remove(pk)
            if res == True:
                return Response({"sms": "Forma de pago de factura eliminada"}, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Se ha generado un error. "+str(res)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)


class FormaPagoFacturaView(LoginRequiredMixin, APIView):
    permission_classes = [IsAuthenticated]

    @action(detail=False, method="POST")
    def post(self, request, format=json):
        if request.user.is_authenticated:
            serializer = FormaPagoFacturaSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="PUT")
    def put(self, request, format=json):

        if request.user.is_authenticated:
            serializer = FormaPagoFacturaSerializer(data=request.data)
            if serializer.is_valid():
                forma_pago_factura = FormaPagoFactura(
                    id=request.data["id"],
                    formaPago=request.data["formaPago"],
                    facturaid=request.data["facturaid"],
                    tiempo=request.data["tiempo"],
                    plazo=request.data["plazo"],
                    valor=request.data["valor"],
                    usuario=request.user
                )
                res = FormaPagoFactura.update(forma_pago_factura)
                if res:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Error": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Error ": "Datos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, method="GET")
    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = FormaPagoFactura.search_id(pk)
                serializer = FormaPagoFacturaSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, method="DELETE")
    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = FormaPagoFactura.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListToFacturaFormaPago(ListAPIView):
    """
    """

    serializer_class = FormaPagoFacturaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated():
            id_factura = self.kwargs["id"]
            return FormaPagoFactura.search_to_id_factura(id_factura)
        else:
            return Response({"Error ": "Acceso no autorizado. "}, status=status.HTTP_401_UNAUTHORIZED)


class FormaPagoNotaDebitoView(LoginRequiredMixin, APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=json):
        if request.user.is_authenticated:
            serializer = FormaPagoNotaDebitoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=json):
        if request.user.is_authenticated:
            serializer = FormaPagoNotaDebitoSerializer(data=request.data)
            if serializer.is_valid():
                forma_pago_factura = FormaPagoNotaDebito(
                    id=request.data["id"],
                    nota_debito=request.data["nota_debito"],
                    forma_pago=request.data["forma_pago"],
                    plazo=request.data["plazo"],
                    valor=request.data["valor"],
                    usuario=request.user
                )
                res = FormaPagoNotaDebito.update(forma_pago_factura)
                if res:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Error": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Error ": "Datos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = FormaPagoNotaDebito.search(pk)
                serializer = FormaPagoNotaDebitoSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = FormaPagoNotaDebito.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FormaPagoNDList(ListAPIView):

    serializer_class = FormaPagoNotaDebitoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            id_nota_debito = self.kwargs["id"]
            return FormaPagoNotaDebito.search_to_nota_debito(id_nota_debito)
        else:
            return Response({"Error ": "Acceso no autorizdo"}, status=status.HTTP_401_UNAUTHORIZED)


class NotaCreditoView(LoginRequiredMixin, APIView):
    """
    API para crud de nota de credito.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, format=json):
        if request.user.is_authenticated:
            try:
                with transaction.atomic():
                    serializer = NotaCreditoSerializer(data=request.data)
                    res = NotaCredito.objects.filter(emisor=request.data["emisor"], establecimiento=request.data[
                                                     "establecimiento"], puntoEmision=request.data["puntoEmision"], secuencia=request.data["secuencia"])
                    
                    if len(res) <= 0:
                        if serializer.is_valid():
                            fecha = request.data["fecha"]
                            emi_temp = Emisor.objects.get(id=request.data["emisor"])
                            est_temp = Establecimiento.objects.get(id = request.data["establecimiento"])
                            pemi_temp = PuntoEmision.objects.get(id = request.data["puntoEmision"])
                            
                            
                            #Para generar el codigo de acceso.
                            access_key = modulo11(
                                fecha, "04", str(emi_temp.identificacion),
                                str(emi_temp.ambiente), str(est_temp.serie), str(pemi_temp.serie),
                                (str(request.data["secuencia"])).zfill(9), "1")
                            print("access_key ",access_key)
                            serializer.save(autorizacion=access_key ,claveacceso=access_key)
                            details = []
                            
                            try:
                                for detail in request.data["detalle_nota_credito"]:
                                    
                                    cantidad_temp = detail["cantidad"]

                                    valorUnitario_temp = detail["valorUnitario"]

                                    descuento_temp = detail["ice"]

                                    ice_temp = detail["ice"]

                                    valorTotal_temp = detail["valorTotal"]

                                    irbpnr_temp = detail["irbpnr"]

                                    notaCredito_temp = NotaCredito(id=serializer.data["id"])

                                    producto_temp = Producto(id=detail["producto"])

                                    usuario_temp = request.user

                                    detnc = DetalleNC(
                                        cantidad=cantidad_temp,
                                        valorUnitario=valorUnitario_temp,
                                        descuento=descuento_temp,
                                        ice=ice_temp,
                                        valorTotal=valorTotal_temp,
                                        irbpnr=irbpnr_temp,
                                        notaCredito=NotaCredito(
                                            id=notaCredito_temp.id),
                                        producto=Producto(id=producto_temp.id),
                                        usuario=usuario_temp
                                    )
                                    print("detnc ", detnc.cantidad)

                                    res = DetalleNC.create(detnc)

                                    print("res ", res)
                                    if type(res) == int:
                                        detnc.id = res
                                        print(detnc)
                                        details.append(detnc)
                                        print(
                                            "detalle de nota de credito guardada")
                                otros = []
                                for otro in request.data["odc_nota_credit"]:
                                    nombre = otro["nombre"]
                                    descripcion = otro["descripcion"]
                                    otrondnc = OtroNDNC(
                                        nombre=nombre,
                                        descripcion=descripcion,
                                        notaCredito=NotaCredito(
                                            id=serializer.data["id"]),
                                        usuario=request.user
                                    )
                                    resp = OtroNDNC.create(otrondnc)

                                    if type(resp) == int:
                                        otros.append(otro)
                                        print("otros guadado nota de credito")
                                serializer.data["odc_nota_credit"] = otros

                            except BaseException as ex:
                                return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                            serData = DetalleNCSerializer(data=details)
                            serializer.data["nota_credito"] = serData
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"Error": "Ya existe un documento con estos datos."}, status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as integrity:
                return Response({"Error": str(integrity)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except BaseException as ex:
                return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=json):
        if request.user.is_authenticated:
            serializer = NotaCreditoSerializer(data=request.data)
            if serializer.is_valid():
                nota_credito = NotaCredito(
                    id=request.data["id"],
                    establecimiento=Establecimiento(
                        id=request.data["establecimiento"]),
                    puntoEmision=PuntoEmision(id=request.data["puntoEmision"]),
                    secuencia=request.data["secuencia"],
                    autorizacion=request.data["autorizacion"],
                    claveacceso=request.data["claveacceso"],
                    fecha=request.data["fecha"],
                    comprobanteModificado=request.data["comprobanteModificado"],
                    establecimientoDoc=request.data["establecimientoDoc"],
                    puntoEmisionDoc=request.data["puntoEmisionDoc"],
                    secuenciaDoc=request.data["secuenciaDoc"],
                    motivo=request.data["motivo"],
                    tarifa0=request.data["tarifa0"],
                    tarifadif0=request.data["tarifadif0"],
                    noObjetoIva=request.data["noObjetoIva"],
                    descuento=request.data["descuento"],
                    excento=request.data["excento"],
                    valorIce=request.data["valorIce"],
                    valorirbpnr=request.data["valorirbpnr"],
                    iva=request.data["iva"],
                    total=request.data["total"],
                    estado=request.data["estado"],
                    emisor=Emisor(id=request.data["emisor"]),
                    cliente=Cliente(id=request.data["cliente"]),
                    usuario=request.user
                )
                res = NotaCredito.update(nota_credito)
                print("res ", res)
                if res:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Error": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Error ": "Datos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = NotaCredito.search(pk)
                serializer = NotaCreditoSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = NotaCredito.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotaCreditoRageEmisor(ListAPIView):

    serializer_class = NotaCreditoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                emisor_id = self.kwargs["id_emisor"]
                date_init = self.kwargs["date_start"]
                date_end = self.kwargs["date_end"]

                print("emisor_id ", emisor_id)
                print("date_init ", date_init)
                print("date_end ", date_end)

                return NotaCredito.list_to_emisor_range(emisor_id, date_init, date_end)
            else:
                return Response({"Error ": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NotaCredidotoSearchSecuencia(ListAPIView):
    """
    API para obtener una nota de credito por su secuencia.
    """
    serializer_class = NotaCreditoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                id_emisor = self.kwargs["id_emisor"]
                est = self.kwargs["establecimiento"]
                p_emi = self.kwargs["p_emision"]
                secuencia = self.kwargs["secuencia"]

                return NotaCredito.search_to_serie(id_emisor, est, p_emi, secuencia)
            else:
                return Response({"Error ": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OtroNDNCView(LoginRequiredMixin, APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=json):
        if request.user.is_authenticated:
            serializer = OtroNDNCSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=json):
        if request.user.is_authenticated:
            serializer = OtroNDNCSerializer(data=request.data)
            if serializer.is_valid():
                nota_credito_otro = OtroNDNC(
                    id=request.data["id"],
                    nombre=request.data["nombre"],
                    descripcion=request.data["descripcion"],
                    notaDebito=request.data["notaDebito"],
                    notaCredito=request.data["notaCredito"],
                    usuario=request.user
                )
                res = OtroNDNC.update(nota_credito_otro)
                if res:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Error": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Error ": "Datos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = OtroNDNC.search(pk)
                serializer = OtroNDNCSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = OtroNDNC.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OtroNDNCListToNC(ListAPIView):

    serializer_class = OtroNDNCSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                tipo_doc = self.kwargs["tipo_doc"]

                id = self.kwargs["id_doc"]

                if tipo_doc == 1:
                    # Para listar los otros de las notas de credito.
                    return OtroNDNC.list_to_nc(id)
                else:
                    # Para listar otros de las notas de debito.
                    return OtroNDNC.list_to_nd(id)
            else:
                return Response({"Error": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetalleNCView(LoginRequiredMixin, APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=json):
        if request.user.is_valid():
            serializer = DetalleNCSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=json):
        if request.user.is_authenticated:
            serializer = DetalleNCSerializer(data=request.data)
            if serializer.is_valid():
                detalle_nc = DetalleNC(
                    id=request.data["id"],
                    cantidad=request.data["cantidad"],
                    valorUnitario=request.data["valorUnitario"],
                    descuento=request.data["descuento"],
                    ice=request.data["ice"],
                    valorTotal=request.data["valorTotal"],
                    irbpnr=request.data["irbpnr"],
                    notaCredito=NotaCredito(id=request.data["notaCredito"]),
                    producto=Producto(id=request.data["producto"]),
                    usuario=request.user
                )
                res = DetalleNC.update(detalle_nc)
                if res:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Error": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Error ": "Datos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = DetalleNC.search(pk)
                serializer = DetalleNCSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = DetalleNC.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetalleNCList(ListAPIView):
    serializer_class = DetalleNCSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                id = self.kwargs["id_nc"]
                return DetalleNC.list_to_nc(id)
            else:
                return Response({"Error ": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetencionCodigoView(LoginRequiredMixin, APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=json):
        if request.user.is_authenticated:
            serializer = RetencionCodigoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=json):
        if request.user.is_authenticated:
            #serializer = RetencionCodigoSerializer(data=request.data)
            try:
                ret_temp = RetencionCodigo.objects.filter(
                    codigo=request.data["codigo"])
                if len(ret_temp) > 0 and ret_temp[0].id == request.data["id"]:
                    retencion = RetencionCodigo(
                        id=request.data["id"],
                        codigo=request.data["codigo"],
                        porcentaje=request.data["porcentaje"],
                        detalle=request.data["detalle"],
                        tipo=request.data["tipo"],
                        usuario=request.user

                    )
                    res = RetencionCodigo.update(retencion)
                    if res:
                        return Response({"Datos actualizados."}, status=status.HTTP_200_OK)
                    else:
                        return Response({"Error": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"Error": "Ya existe este c??digo registrado."}, status=status.HTTP_400_BAD_REQUEST)
            except BaseException as ex:
                return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = RetencionCodigo.search(pk)
                serializer = RetencionCodigoSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = RetencionCodigo.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetencionCodigoGet(ListAPIView):

    serializer_class = RetencionCodigoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                codigo = self.kwargs["codigo"]
                if codigo == "0":
                    return RetencionCodigo.list_all()
                return RetencionCodigo.search_to_codigo(codigo)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetencionView(LoginRequiredMixin, APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=json):
        if request.user.is_authenticated:
            try:
                with transaction.atomic():
                    serializer = RetencionSerializer(data=request.data)
                    
                    if serializer.is_valid():
                        if len(Retencion.objects.filter(
                            emisor=request.data["emisor"],
                            sujeto_retenido=request.data["sujeto_retenido"],
                            establecimiento=request.data["establecimiento"],
                            pemision=request.data["pemision"],
                            secuencia=request.data['secuencia']
                        )) <= 0:
                            fecha = request.data["fecha"]
                            emi_temp = Emisor.objects.get(id=request.data["emisor"])
                            est_temp = Establecimiento.objects.get(id = request.data["establecimiento"])
                            pemi_temp = PuntoEmision.objects.get(id = request.data["pemision"])
                            
                            
                            #Para generar el codigo de acceso.
                            access_key = modulo11(
                                fecha, "07", str(emi_temp.identificacion),
                                str(emi_temp.ambiente), str(est_temp.serie), str(pemi_temp.serie),
                                (str(request.data["secuencia"])).zfill(9), "1")
                            
                            serializer.save(autorizacion=access_key,clave_acceso=access_key)
                            
                            for retencion in request.data["retenciones_compra"]:
                                baseImponible = retencion["baseImponible"]
                                valor_retenido = retencion["valor_retenido"]
                                retencion_codigo = RetencionCodigo(
                                    id=retencion["retencion_codigo"])
                                retencion = Retencion(id=serializer.data["id"])
                                emisor = Emisor(id=serializer.data["emisor"])
                                usuario = request.user

                                result = RetencionCompra(
                                    baseImponible=baseImponible,
                                    valor_retenido=valor_retenido,
                                    retencion=retencion,
                                    retencion_codigo=retencion_codigo,
                                    emisor=emisor,
                                    usuario=usuario,
                                )
                                res = Retencion.create(result)
                                print("Guardado ", res)
                            
                            return Response(serializer.data, status=status.HTTP_201_CREATED)
                        else:
                            return Response({"Error": "Ya existe una retenci??n con estos datos."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            except IntegrityError as integrity:
                return Response({"Error": str(integrity)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except BaseException as ex:
                return Response({"Error": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=json):
        if request.user.is_authenticated:
            serializer = RetencionSerializer(data=request.data)
            if serializer.is_valid():
                retencion = Retencion(
                    id=request.data["id"],
                    emisor=Emisor(id=request.data["emisor"]),
                    sujeto_retenido=Cliente(
                        id=request.data["sujeto_retenido"]),
                    establecimiento=Establecimiento(
                        id=request.data["establecimiento"]),
                    pemision=PuntoEmision(id=request.data["pemision"]),
                    secuencia=request.data["secuencia"],
                    fecha=request.data["fecha"],
                    tipo_documento=request.data["tipo_documento"],
                    estab_doc=request.data["estab_doc"],
                    pemis_doc=request.data["pemis_doc"],
                    secuencia_doc=request.data["secuencia_doc"],
                    autorizacion=request.data["autorizacion"],
                    clave_acceso=request.data["clave_acceso"],
                    usuario=request.user
                )
                res = Retencion.update(retencion)
                if res:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"Error": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Error ": "Datos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = Retencion.search(pk)
                serializer = RetencionSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = Retencion.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetencionSecuencia(ListAPIView):
    serializer_class = RetencionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                id_emi = self.kwargs["id_emisor"]
                est = self.kwargs["est"]
                pemi = self.kwargs["pemi"]
                secu = self.kwargs["secuencia"]

                return Retencion.search_to_secuencia(id_emi, est, pemi, secu)
            else:
                return Response({"Error ": "Acceso no autorizado"}, status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetencionEmisorRange(ListAPIView):

    serializer_class = RetencionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            if self.request.user.is_authenticated:
                emisor_id = self.kwargs['emisor_id']
                date_start = self.kwargs["date_start"]
                date_end = self.kwargs["date_end"]
                
                return Retencion.list_to_emisor_range(emisor_id, date_start, date_end)
            else:
                return Response({"Error":"Acceso no autorizado."},status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            print("error ",ex)
            return Response({"Error":str(ex)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RetencionCompraView(LoginRequiredMixin, APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=json):
        if request.user.is_authenticated:
            serializer = RetencionCompraSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, format=json):
        if request.user.is_authenticated:
            serializer = RetencionCompraSerializer(data=request.data)
            if serializer.is_valid():
                retencion = RetencionCompra(
                    id=request.data["id"],
                    baseImponible=request.data["baseImponible"],
                    valor_retenido=request.data["valor_retenido"],
                    retencion=Retencion(id=request.data["retencion"]),
                    retencion_codigo=RetencionCodigo(id=request.data["retencion_codigo"]),
                    emisor=Emisor(id=request.data["emisor"]),
                    usuario=request.user
                )
                res = RetencionCompra.update(retencion)
                
                if res:
                    return Response({"Datos actualizados."},status=status.HTTP_200_OK)
                else:
                    return Response({"Error":str(res)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            else:
                return Response({"Error ": "Datos invalidos"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error ": "Acceso no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                #res = Retencion.search(pk)
                #res = RetencionCompra.search_to_retencion(pk)
                res = RetencionCompra.search(pk)
                print("res ", res)
                serializer = RetencionCompraSerializer(res, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, pk):
        try:
            if request.user.is_authenticated:
                res = RetencionCompra.remove(pk)
                if res:
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"Error ": str(res)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except BaseException as ex:
            return Response({"Error ": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GenerateSecuenceDocument(LoginRequiredMixin, APIView):
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, method="GET")
    def get(self, request, *args,**kwargs):
        tipo_doc = self.kwargs["tipo_doc"]
        id_emisor = self.kwargs["id_emisor"]
        establecimiento = self.kwargs["establecimiento"]
        p_emision = self.kwargs["p_emision"]
        
        #1 Factura.
        #2 Nota de credito.
        #3 Nota de debito.
        #4 Retencion.
        
        #val  = modulo11("2022-04-08", "01", "0106405236001", "1", "001", "001", "000000001", "1")
        
        if (request.user.is_authenticated):
            try:
                emisor_temp = Emisor.objects.get(id=id_emisor)
                
                try:
                    establecimiento_temp = Establecimiento.objects.get(id=establecimiento)
                    
                    try:
                        p_emision_temp = PuntoEmision.objects.get(id=p_emision)
                    except PuntoEmision.DoesNotExist as pemi:
                        logger.error(pemi)
                        return Response({"Error":"No existe el punto de emision solicitado."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        
                    if tipo_doc ==1:
                        fact = FacturaCabecera.objects.filter(
                            establecimiento=establecimiento_temp.id,
                            punto_emision=p_emision_temp.id, 
                            emisor=emisor_temp.id
                        ).order_by('secuencia').latest('secuencia')
                        nueva_factura = int(fact.secuencia)+1
                        return Response({"SMS":"Nueva secuencia","SECUENCIA":nueva_factura}, status=status.HTTP_200_OK)
                    if tipo_doc==2:
                        nota_credito = NotaCredito.objects.filter(
                            establecimiento=establecimiento_temp.id,
                            puntoEmision = p_emision_temp.id,
                            emisor=emisor_temp.id
                        ).order_by('secuencia').latest('secuencia')
                        nueva_nc_serie = int(nota_credito.secuencia)+1
                        return Response({"SMS":"Nueva secuencia","SECUENCIA":nueva_nc_serie}, status=status.HTTP_200_OK)
                    if tipo_doc==3:
                        nota_debito = NotaDebito.objects.filter(
                            establecimiento=establecimiento_temp.id,
                            puntoEmision = p_emision_temp.id,
                            emisor=emisor_temp.id
                        ).order_by('secuencia').latest("secuencia")
                        nota_debito_serie = int(nota_debito.secuencia)+1
                        return Response({"SMS":"Serie generada nota de debito. ","SECUENCIA":nota_debito_serie}, status=status.HTTP_200_OK)
                    if tipo_doc==4:
                        retencion = Retencion.objects.filter(
                            establecimiento=establecimiento_temp.id,
                            pemision = p_emision_temp.id,
                            emisor=emisor_temp.id
                        ).order_by('secuencia').latest('secuencia')
                        nueva_retencion = int(retencion.secuencia)+1
                        return Response({"SMS":"Serie generada retencion. ","SECUENCIA":nueva_retencion}, status=status.HTTP_200_OK)
                    else:
                        return Response({"SMS":"No se ha recibido un tipo de documento valido. "}, status=status.HTTP_200_OK)
                except Establecimiento.DoesNotExist as est:
                    logger.error(est)
                    return Response({"Error":"No existe el establecimiento solicitado. "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
                    
                    
            except Emisor.DoesNotExist:
                return Response({"Error":"No existe el emisor solicitado. "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
        else:
            return Response({"Error":"Serie generada. "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

def modulo11(fecha, tipo_comp, numero_ruc_cliente, ambiente, establecimiento, pemision, secuencia, tipo_emision):
    """
    Metodo para generar la clave de acceso.
    """
    codigo = "20220408"
    
    if len(fecha)==10 and len(tipo_comp)==2 and len(numero_ruc_cliente)==13 and len(ambiente)==1 \
        and len(establecimiento)==3 and len(pemision)==3 and len(secuencia)==9 \
        and len(tipo_emision)==1:
        dv = 0
            
        arr_fecha = fecha.split("-")
        anio=arr_fecha[0]
        month = arr_fecha[1]
        day = arr_fecha[2]
        
        digit_part = day+month+anio+tipo_comp+numero_ruc_cliente+ambiente+establecimiento+pemision+secuencia+tipo_emision+codigo
        
        arr_digitos = list(digit_part)
        
        sum = 0
        factor =2
        for digit in arr_digitos:
            sum = sum + (int(digit) * factor)
            if factor ==7:
                factor = 2
            else:
                factor=+1
        
        dv = 11 - (sum % 11)
        
        if dv ==10:
            return 1
        if dv == 11:
            return 0
        
        digit_part=digit_part+str(dv)
        return digit_part
    else:
        return "La longitud de los campos no es valida."
    
    