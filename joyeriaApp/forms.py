from django import forms
from .models import Marca,Articulo
from django.forms import ModelForm, Textarea

class ArticuloForm(forms.ModelForm):
    class Meta:
            model = Articulo
            # fields = ('modelo', 'descripcion','imagen','articulo_marca')
            fields = '__all__'
            widgets = {
                'descripcion': Textarea(attrs={'cols': 40, 'rows': 10}),
            }
    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        self.fields['articulo_marca'].label = "Marca"

class MarcaForm(forms.ModelForm):
    class Meta:
            model = Marca
            fields = ('nombre',)
            error_messages = {
                'nombre': {
                    'unique': "El nombre de la marca debe ser unico.",
                },
            }