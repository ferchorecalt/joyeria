# -*- coding: utf-8 -*-
from django import forms
from .models import Marca,Articulo
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Nombre de usuario"
        self.fields['username'].help_text="Requerido. Hasta 150 caracteres. Letras, digitos y @/./+/-/_ solamente."
        self.fields['username'].error_messages = {'invalid': 'El usuario ingresado ya existe'}
        self.fields['username'].error_messages = {'required': 'El campo es obligatorio. Se pueden ingresar letras, digitos y @/./+/-/_ unicamente'}
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Repita la contraseña"
        self.fields['password1'].error_messages = {'required': 'La contraseña es obligatoria'}
        self.fields['password2'].error_messages = {'required': 'La contraseña es obligatoria'}
        self.fields['password2'].help_text="Repita la contraseña, para verificacion."


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
            field.error_messages = {'required':'El campo {fieldname} es requerido'.format(fieldname=field.label)}


class MarcaForm(forms.ModelForm):
    class Meta:
            model = Marca
            # fields = ('nombre',)
            fields = '__all__'
            error_messages = {
                'nombre': {
                    'unique': "El nombre de la marca ya existe!",
                    'required':'Debe ingresar un nombre de marca!',
                },
            }
    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required':'El campo {fieldname} es requerido'.format(fieldname=field.label)}

class ContactForm(forms.Form):
    nombre = forms.CharField(required=True)
    mail = forms.EmailField(required=True)
    asunto = forms.CharField(required=True)
    mensaje = forms.CharField(
        required=True,
        widget=forms.Textarea
    )