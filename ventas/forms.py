
from django import forms
from django.contrib.auth.models import User

from ventas.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','username','first_name', 'last_name', 'password')
        
        
class EmisorForm(forms.ModelForm):
    class Meta:
        model = Emisor
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
        labels = {
            "id":"id",
            "identificacion":"Identificación",
            "tipo_id":"tipo_id",
            "rasonSocial":"rasonSocial",
            "nombreComercial":"nombreComercial",
            "telefono":"telefono",
            "direccionMatriz":"direccionMatriz",
            "contribuyenteEspecial":"contribuyenteEspecial",
            "obligadoLlevarContabilidad":"obligadoLlevarContabilidad",
            "regimenMicroempresa":"regimenMicroempresa",
            "agenteRetencion":"agenteRetencion",
            "logo":"logo",
            "ambiente":"ambiente",
            "tipoToken":"tipoToken",
            "firma":"firma",
            "estado":"estado",
            "cantidad_usuario":"cantidad_usuario",
            "usuario":"usuario",
        }