from django import forms
from mptt.forms import TreeNodeChoiceField

from .models import *


class ContenidoNewForm(forms.ModelForm):
    categoria = TreeNodeChoiceField(queryset=Categoria.objects.all(), level_indicator=u'+--')

    class Meta:
        model = Contenido
        fields = ['titulo', 'copete', 'detalle', 'categoria', 'fecha_publicacion', 'activo', 'recomendado', 'imagen', 'documento']

    def clean_categoria(self):
        categoria = self.cleaned_data['categoria']
        if not categoria.is_leaf_node():
            raise forms.ValidationError("La Categoria no es la correcta.")
        return categoria


class DocumentoNewForm(forms.ModelForm):

    class Meta:
        model = Documento
        fields = ['file',]
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': 'true'})
        }


class GaleriaNewForm(forms.ModelForm):

    class Meta:
        model = Galeria
        exclude = []


class GaleriaImagenNewForm(forms.ModelForm):

    class Meta:
        model = GaleriaImagen
        fields = ['file', ]
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': 'true'})
        }


class SliderForm(forms.ModelForm):

    class Meta:
        model = Slider
        fields = ['texto', 'texto_enlace', 'enlace', 'file', 'posicion', 'activa']
