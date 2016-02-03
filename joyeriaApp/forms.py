from django import forms
from .models import Marca,Articulo
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User


class ArticuloForm(forms.ModelForm):
    class Meta:
            model = Articulo
            # fields = ('modelo', 'descripcion','imagen','articulo_marca')
            fields = '__all__'
            widgets = {
                'descripcion': Textarea(attrs={'cols': 40, 'rows': 10, 'placeholder': 'Ingrese una breve descripcion del articulo a ofrecer'}),
            }
    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        self.fields['articulo_marca'].label = "Marca"
        for field in self.fields.values():
            field.widget.attrs.update({'class' : 'separados'})
            field.error_messages = {'required':'El campo {fieldname} es requerido'.format(
                fieldname=field.label)}

class MarcaForm(forms.ModelForm):
    class Meta:
            model = Marca
            fields = ('nombre',)
            error_messages = {
                'nombre': {
                    'unique': "El nombre de la marca ya existe!",
                    'required':'Debe ingresar un nombre de marca!',
                },
            }
    def __init__(self, *args, **kwargs):
         super(MarcaForm, self).__init__(*args, **kwargs)
         self.fields['nombre'].widget.attrs.update({'class' : 'separados'})

