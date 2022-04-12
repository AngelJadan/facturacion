import xml.etree.ElementTree as ET

from ventas.models import FacturaCabecera

def generate_factura_xml(self, id=int, ambiente = str):
    factura = FacturaCabecera.objects.get(id=id)
    ambiente = 'PRODUCCIÓN'
    if ambiente == '2':
        ambiente = 'PRUEBA'
    
    root = ET.Element('comprobante')
    infoTributaria = ET.SubElement(root, "infoTributaria")
    ambiente = ET.SubElement(infoTributaria, "ambiente")
    ambiente.text = ambiente
    
    tipoEmision = ET.SubElement(infoTributaria, "tipoEmision")
    tipoEmision.text = 1
    
    razonSocial = ET.SubElement(infoTributaria, "razonSocial")
    razonSocial.text = factura.emisor.identificacion
    
    nombreComercial = ET.SubElement(infoTributaria, "nombreComercial")
    nombreComercial.text = factura.emisor.nombreComercial
    
    ruc = ET.SubElement(infoTributaria, "ruc")
    ruc.text = factura.emisor.identificacion
    
    claveAcceso =  ET.SubElement(infoTributaria, "claveAcceso")
    claveAcceso.text = factura.emisor.claveacceso
    
    codDoc = ET.SubElement(infoTributaria, "codDoc")
    codDoc.text = "01"
    
    estab = ET.SubElement(infoTributaria, "estab")
    estab.text = factura.establecimiento.serie
    
    ptoEmi = ET.SubElement(infoTributaria, "ptoEmi")
    ptoEmi.text = factura.punto_emision.serie
    
    secuencial = ET.SubElement(infoTributaria, "secuencia")
    secuencial.text = str(factura.secuencia).zfill(9)
    
    dirMatriz = ET.SubElement(infoTributaria, "dirMatriz")
    dirMatriz.text = factura.emisor.direccionMatriz
    
    
    infoFactura = ET.SubElement(root, "infoFactura")
    fechaEmision = ET.SubElement(infoFactura, "fechaEmision")
    fechaEmision.text = factura.fecha
    
    dirEstablecimiento = ET.SubElement(infoFactura, "dirEstablecimiento")
    dirEstablecimiento.text = factura.establecimiento.direccion
    
    contribuyenteEspecial = ET.SubElement(infoFactura, "contribuyenteEspecial")
    contribuyenteEspecial.text = factura.emisor.contribuyenteEspecial
    
    obligadoContabilidad = ET.SubElement(infoFactura, "obligadoContabilidad")
    if factura.emisor.obligadoLlevarContabilidad:
        obligadoContabilidad.text = "SI"
    else:
        obligadoContabilidad.text = "NO"
    
    
    tipoIdentificacionComprador = ET.SubElement(infoFactura, "tipoIdentificacionComprador")
    tipoIdentificacionComprador.text = factura.cliente.tipoIdentificacion
    
    razonSocialComprador = ET.SubElement(infoFactura, "razonSocialComprador")
    razonSocialComprador.text = factura.cliente.nombreApellido
    
    identificacionComprador = ET.SubElement(infoFactura, "identificacionComprador")
    identificacionComprador.text = factura.cliente.identificacion
    
    totalSinImpuestos = ET.SubElement(infoFactura, "totalSinImpuestos")
    subtotal = float(factura.noobjetoiva) + float(factura.tarifa0) + float(factura.tarifadif0) + float(factura.excentoiva)
    totalSinImpuestos.text = str("{0:.2f}".format(round(subtotal, 2)))
    
    totalDescuento = ET.SubElement(infoFactura, "totalDescuento")
    totalDescuento.text = str("{0:.2f}".format(round(factura.totaldescuento,2)))
    
    totalConImpuestos = ET.SubElement(infoFactura, "totalConImpuestos")
    totalImpuesto = ET.SubElement(totalConImpuestos, "totalImpuesto")
    codigo = ET.SubElement(totalImpuesto, "codigo")
    codigo.text = str("{0:.2f}".format(round(factura.tipo_iva.codigo,2)))
    
    codigoPorcentaje = ET.SubElement(totalImpuesto, "codigoPorcentaje")
    codigoPorcentaje.text = str("{0:.2f}".format(round(factura.tipo_iva.porcentaje,2)))
    
    baseImponible =  ET.SubElement(totalImpuesto, "baseImponible")
    baseImponible.text = str("{0:.2f}".format(round(factura.tarifadif0, 2)))
    
    valor = ET.SubElement(totalImpuesto, "valor")
    valor.text = str("{0:.2f}".format(round(factura.valor_iva)))
    
    
    
    
    
    
    
    pass


