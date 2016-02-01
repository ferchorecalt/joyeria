from django import forms

class ArticuloForm(forms.Form):
    modelo = forms.CharField(label='Modelo',required=True)
    descripcion = forms.CharField(label='Descripcion',required=True)
    imagen = forms.ImageField(required=True)

class MarcaForm(forms.Form):
    nombre = forms.CharField(required=True)