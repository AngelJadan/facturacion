def apply_digital_signature(self, cr, uid, factura, claveAcceso):
        """
        Metodo que aplica la firma digital al XML
        """
        ds_document = False
        tree = etree.ElementTree(factura)
        name = '%s%s.xml' %('/opt/facturas/', claveAcceso)
        tree.write(name, pretty_print=True, xml_declaration=True, encoding='utf-8', method="xml")
        #firma electrónica del xml
        firma_path = os.path.join(os.path.dirname(__file__), 'firma/prctXadesBes.jar')
        #CLINICA METROPOLITANA
        file_pk12 = 'L29wdC9jZXJ0aWZpY2Fkb3Mvam9yZ2VfamF2aWVyX2ppcm9uX3Jvc2Vyby5wMTI='
        password = 'eHRwcTg4MDBNZXRybw=='
        #PEDRO RODRIGUEZ
        #file_pk12 = 'L29wdC9jZXJ0aWZpY2Fkb3MvcGVkcm9fYWx2YXJvX3JvZHJpZ3Vlel9yb3Nlcm8ucDEy'
        #password = 'UENCNzMxOWFndWlsYQ=='
        #invocación del jar de la firma electrónica
        subprocess.call(['java', '-jar', firma_path, name, name, file_pk12, password])
        return ds_document

def action_generate_einvoice(self, cr, uid, ids, context=None):
        """
	@@ -299,20 +318,8 @@ def action_generate_einvoice(self, cr, uid, ids, context=None):
            #validación del xml
            self.validate_xml(cr, uid, factura)

            # firma de XML, now what ??
            ds_invoice = self.apply_digital_signature(cr, uid, factura)"""