from django import forms
from .models import Marca,Articulo

class ArticuloForm(forms.ModelForm):
    class Meta:
            model = Articulo
            fields = ('modelo', 'descripcion','imagen',)


class MarcaForm(forms.ModelForm):
    class Meta:
            model = Marca
            fields = ('nombre',)