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
    
    #Factura detalle
    path("factura_detalle/", views.FacturDetalleViews.as_view(), name ="factura_detalle"),
    path("factura_detalle/<int:pk>/", views.FacturDetalleViews.as_view(), name ="factura_detalle_pk"),
    
    
    #FormaPago
    path("forma_pago/", views.FormaPagoView.as_view(), name ="forma_pago"),
    path("forma_pago/<int:pk>/", views.FormaPagoView.as_view(), name ="forma_pago_pk"),
    
    #FormaPagoFactura
    path("forma_pago_factura/", views.FormaPagoFacturaView.as_view(), name ="forma_pago_factura"),
    path("forma_pago_factura/<int:pk>/", views.FormaPagoFacturaView.as_view(), name ="forma_pago_factura_id"),
    
    #Otro
    path("otro/", views.OtroViews.as_view(), name ="otro"),
    path("otro/<int:pk>/", views.OtroViews.as_view(), name ="otro"),
    
    
]
