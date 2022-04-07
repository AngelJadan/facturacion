from django.contrib import admin
from django.urls import path
from ventas import views

urlpatterns = [
    path('register_user/', views.RegisterUsers.as_view(),name="register"),
    path('login/',views.Login.as_view(),name="login"),
    path('logout/',views.Logout.as_view(),name="logout"),
    path('emisor_view/', views.EmisorView.as_view(),name="emisor_view"),
    path('get_emisor_id/<int:id>/', views.EmisorGetId.as_view(), name="get_emisor_id"),
    path('emisor_disable/<int:pk>/', views.EmisorDisable.as_view(), name="emisor_disable"),
    path('emisor_get_identificacion/<str:identificacion>/', views.EmisorGetIdentificacion.as_view(), name="emisor_get_identificacion"),
    path('emisor_update/', views.EmisorUpdate.as_view(), name="emisor_update"),
    
    #Establecimientos
    path('establecimiento/', views.EstablecimientoCreate.as_view(), name="establecimiento"),#Para crear(POST) y actualizar(PUT), 
    path('establecimiento/<int:pk>/', views.EstablecimientoCreate.as_view(), name="establecimiento_get_id_emisor"),#Para obtener un establecimiento por el id de un emisor
    #path('establecimiento$/<int:id_establecimiento>/', views.EstablecimientoCreate.as_view(), name="establecimiento_get_id_establecimiento"),#Para eliminar un etablecimiento por su id
    
    
    #Puntos de emision
    path('punto_emision/', views.PuntoEmisionViews.as_view(), name="punto_emision"),#Para crear y actualizar un punto de emision
    path('punto_emision/<int:id_puntoemision>/', views.PuntoEmisionViews.as_view(), name="punto_emision_id"),#Para obtener un punto de emision(GET), para eliminar un punto de emsion(DELETE)
    path('punto_emision_to_establecimiento/<int:establecimiento_id>/',views.PuntoEmisionList.as_view(), name="punto_emision_to_establecimiento"),#Para listar los puntos de emision de un establecimiento
    
    #Clientes
    path('cliente/', views.ClienteViews.as_view(), name="cliente"),#Para registrar (POST) y actualizar un cliente (PUT)
    path('cliente/<int:pk>/', views.ClienteViews.as_view(), name="cliente_emisor_id"), #Para obtener un cliente por su id
    path('cliente_to_emisor/<int:pk>/', views.ListClienteToEmisor.as_view(), name="cliente_to_emisor"),#Para listar los clientes de  un emisor (GET)
    
    #Iva
    path("iva/",views.IvaViews.as_view(), name="iva"),#Para crear(POST) y actualizar(PUT) el iva
    path("iva/<int:pk>/", views.IvaViews.as_view(), name="iva_pk"),#Para obtener y listar un iva.
    path("iva/list/", views.ListIva.as_view(), name="iva_list"),#Para listar todos los ivas
    
    #Producto
    path("producto/",views.ProductoViews.as_view(), name ="producto"),
    path("producto/<int:pk>/", views.ProductoViews.as_view(), name ="producto_pk"),
    path("producto_list/<int:emisor_id>/", views.ProductoListEmisor.as_view(), name="producto_list"),#Para
    
    #Factura
    path("factura/", views.FacturaView.as_view(), name ="factura"),
    path("factura/<int:pk>/", views.FacturaView.as_view(), name ="factura"),
    
    
    #FormaPago
    path("forma_pago/", views.FormaPagoView.as_view(), name ="forma_pago"),
    path("forma_pago/<int:pk>/", views.FormaPagoView.as_view(), name ="forma_pago_pk"),
    
    
    #FormaPagoFactura
    path("forma_pago_factura/", views.FormaPagoFacturaView.as_view(), name ="forma_pago_factura"),
    path("forma_pago_factura/<int:pk>/", views.FormaPagoFacturaView.as_view(), name ="forma_pago_factura_id"),
    path("factura_list_emisor_range_date/<int:id_emisor>/<str:date_init>/<str:date_end>/", views.FacturaListEmisorRangeDate.as_view(), name ="factura_list_emisor_range_date"),
    path("factura_list_emisor_month/<int:id_emisor>/<str:month>/<str:year>/", views.FacturaListEmisorMonth.as_view(), name ="factura_list_emisor_month"),
    #path("list_to_factura_formapago/", views.ListToFacturaFormaPago.as_view(), name="list_to_factura_formapago"),
    
    #Factura detalle
    path("factura_detalle/", views.FacturDetalleViews.as_view(), name ="factura_detalle"),
    path("factura_detalle/<int:pk>/", views.FacturDetalleViews.as_view(), name ="factura_detalle_pk"),
    
    
    #NotaDebito
    path("nota_debito/", views.NotaDebitoView.as_view(), name ="nota_debito"),
    path("nota_debito/<int:pk>/", views.NotaDebitoView.as_view(), name ="nota_debito_pk"),
    path("list_nota_debito_emisor_range/<int:id_emisor>/<str:start>/<str:end>/", views.ListNotaDebitoEmisorRange.as_view(), name ="list_nota_debito_range"),
    
    #Otro
    path("otro/", views.OtroViews.as_view(), name ="otro"),
    path("otro/<int:pk>/", views.OtroViews.as_view(), name ="otro"),
    path("list_to_factura_otros/<int:id_factura>/", views.ListToFacturaOtros.as_view(), name ="list_to_factura_otros"),
    
    
    #Formas de pagos Nota de debito.
    path("forma_pago_nota_debito_view/", views.FormaPagoNotaDebitoView.as_view(), name ="forma_pago_nota_debito"),
    path("forma_pago_nota_debito_view/<int:pk>/", views.FormaPagoNotaDebitoView.as_view(), name ="forma_pago_nota_debito_pk"),
    path("forma_pagond_list/<int:id>/", views.FormaPagoNDList.as_view(), name ="forma_pagond_list"),
    
    
    #Nota de creditos
    path('nota_creditoview/', views.NotaCreditoView.as_view(), name ="nota_creditoview"),
    path('nota_creditoview/<int:pk>/', views.NotaCreditoView.as_view(), name ="nota_creditoview_pk"),
    path('list_nota_credito_range/<int:id_emisor>/<str:date_start>/<str:date_end>/', views.NotaCreditoRageEmisor.as_view(), name ="list_nota_credito_range"),
    path('nota_credidoto_search_secuencia/<int:id_emisor>/<str:establecimiento>/<str:p_emision>/<int:secuencia>/', views.NotaCredidotoSearchSecuencia.as_view(), name="nota_credidoto_search_secuencia"),
    
    
    #Otros Nota de debito o Nota de credito.
    path("otro_ndncview/", views.OtroNDNCView.as_view(), name = "otro_ndncview"),
    path("otro_ndncview/<int:pk>/", views.OtroNDNCView.as_view(), name = "otro_ndncview_pk"),
    path('otrondnc_list_to_nc/<int:tipo_doc>/<int:id_doc>/', views.OtroNDNCListToNC.as_view(), name ="otrondnc_list_to_nc"),
    
    #Detalle nota de credito
    path("detallencview/", views.DetalleNCView.as_view(), name ="detallencview"),
    path("detallencview/<int:pk>/", views.DetalleNCView.as_view(), name ="detallencview_pk"),
    path("detallenc_list/<int:id_nc>/", views.DetalleNCList.as_view(), name ="detallenc_pk"),
    
    #Retencion Codigos
    path("retencion_codigo/", views.RetencionCodigoView.as_view(), name ="retencioncodigo"),
    path("retencion_codigo/<int:pk>/", views.RetencionCodigoView.as_view(), name ="retencioncodigo_pk"),
    path("retencion_codigo_get/<str:codigo>/", views.RetencionCodigoGet.as_view(), name ="retencioncodigo_get"),
    
    #Retencion
    path("retencion/", views.RetencionView.as_view(), name ="retencion"),
    path("retencion/<int:pk>/", views.RetencionView.as_view(), name ="retencion_pk"),
    path("retencion_secuencia/<int:id_emisor>/<str:est>/<str:pemi>/<int:secuencia>/", views.RetencionSecuencia.as_view(), name ="retencion_secuencia"),
    path("retencion_emisor_range/<int:emisor_id>/<str:date_start>/<str:date_end>/", views.RetencionEmisorRange.as_view(), name ="retencion_emisor_range"),
    
    
    #Retencion de compras.
    path("retencion_compra/", views.RetencionCompraView.as_view(), name ="retencion_compra"),
    path("retencion_compra/<int:pk>/", views.RetencionCompraView.as_view(), name ="retencion_compra_pk"),
    
    
    
    
    
    
    
    
    
    
    
    
    
]
