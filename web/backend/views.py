from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView, DetailView, CreateView, DeleteView
from django.template.loader import render_to_string
from PIL import Image

from django.contrib.auth.models import User
from .models import *
from .forms import *


#
# Usuario
#
class UsuarioListView(ListView):
    model = User
    context_object_name = 'usuarios'
    template_name = 'backend/usuario_list.html'


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Usuario creado correctamente.')
            return HttpResponseRedirect(reverse('backend:usuario_list'))

    else:
        f = UserCreationForm()

    return render(request, 'registration/register.html', {'form': f})


def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'La contraseña del usuario fue actualizada.')
            return HttpResponseRedirect(reverse('backend:usuario_list'))
        else:
            messages.error(request, 'Favor corregir el problema.')
    else:
        form = SetPasswordForm(user)
    return render(request, 'registration/password_change_form.html', {
        'form': form
    })


#
# Contenido
#
class ContenidoListView(ListView):
    model = Contenido
    context_object_name = 'contenidos'
    template_name = 'backend/contenido_list.html'


@login_required()
def contenido_new(request):
    if request.method == 'POST':
        form = ContenidoNewForm(request.POST, request.FILES)
        if form.is_valid():
            contenido = form.save(commit=False)
            contenido.user = request.user
            contenido.save()
            return HttpResponseRedirect(reverse('backend:contenido_list'))
        else:
            form = ContenidoNewForm(request.POST)
    else:
        form = ContenidoNewForm()
    ctx = {'form': form}
    return render(request, 'backend/contenido_new.html', ctx)


class ContenidoEditView(SuccessMessageMixin, UpdateView):
    model = Contenido
    form_class = ContenidoNewForm
    template_name = 'backend/contenido_new.html'
    success_message = 'Contenido editado correctamente.'
    success_url = reverse_lazy('backend:contenido_list')


class ContenidoDeleteView(DeleteView):
    model = Contenido
    pk_url_kwarg = 'pk'
    success_message = 'Contenido eliminado correctamente.'
    success_url = reverse_lazy('backend:contenido_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ContenidoDeleteView, self).delete(request, *args, **kwargs)


@login_required()
def categoria_leaf_node(request):
    categoria_id = request.GET.get('categoria')

    data = {
        'is_leaf': Categoria.objects.get(id=categoria_id).is_leaf_node()
    }

    return JsonResponse(data)


class BasicUploadView(View):

    def get(self, request):
        documentos = Contenido.objects.all()
        return render(self.request, 'backend/documento_upload.html', {'documentos': documentos})

    def post(self, request):
        form = DocumentoNewForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            documento = form.save()
            print(documento.file.name.split('/'))
            print(documento.file.url)
            data = {'is_valid': True, 'documento': documento.file.name.split('/')[1], 'url': documento.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


#
# Galeria
#
class GaleriaListView(ListView):
    model = Galeria
    context_object_name = 'galerias'
    template_name = 'backend/galeria_list.html'
    queryset = Galeria.objects.all().order_by('-creada')


class GaleriaCreateView(CreateView):
    model = Galeria
    fields = ['titulo', 'descripcion', 'activa', 'recomendada']
    template_name = 'backend/galeria_new.html'


@login_required()
def galeria_edit(request, pk):
    galeria = get_object_or_404(Galeria, id=pk)
    if request.method == 'POST':
        form = GaleriaNewForm(request.POST, instance=galeria)
        if form.is_valid():
            g = form.save()
            messages.success(request, 'Galeria ' + g.titulo.upper() + ' actualizada correctamente.')
            return HttpResponseRedirect(reverse('backend:galeria_list'))
        else:
            form = GaleriaNewForm(request.POST)
    else:
        form = GaleriaNewForm(instance=galeria)
    ctx = {'form': form, 'galeria': galeria, 'imagenes': galeria.imagenes.all()}
    return render(request, 'backend/galeria_edit.html', ctx)


class GaleriaDeleteView(DeleteView):
    model = Galeria
    pk_url_kwarg = 'pk'
    template_name = 'backend/galeria_confirm_delete.html'
    success_url = reverse_lazy('backend:galeria_list')

    def get_object(self, queryset=None):
        galeria_id = self.kwargs['pk']
        queryset = Galeria.objects.get(id=galeria_id)

        if not queryset:
            raise Http404

        ctx = {'galeria': queryset}
        return ctx

    def delete(self, request, *args, **kwargs):
        galeria_id = self.kwargs['pk']
        galeria = Galeria.objects.get(id=galeria_id)

        for imagen in galeria.imagenes.all():
            imagen.delete()
        galeria.delete()

        messages.info(request, 'Galeria borrada correctamente.')
        return HttpResponseRedirect(reverse('backend:galeria_list'))


@login_required()
def imagen_delete(request, pk):
    imagen = get_object_or_404(GaleriaImagen, id=pk)
    galeria_id = imagen.galeria.id
    data = dict()
    print(imagen.id)
    if request.method == 'POST':
        imagen.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        imagenes = GaleriaImagen.objects.filter(galeria_id__exact=galeria_id)
        data['html_imagen_list'] = render_to_string('backend/imagen_list_partial_upload.html', {'imagenes': imagenes})
    else:
        ctx = {'imagen': imagen}
        data['html_form'] = render_to_string('backend/imagen_delete_partial.html', ctx, request=request)
    return JsonResponse(data)


class ImagenUploadView(View):
    # def get(self, request, galeria_id):
    #     imagenes = GaleriaImagen.objects.filter(galeria_id__exact=id)
    #     print(imagenes)
    #     return render(self.request, 'backend/documento_upload.html', {'imagenes': imagenes})

    def post(self, request, pk):
        form = GaleriaImagenNewForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.galeria_id = pk
            imagen.save()

            with Image.open(imagen.file) as i:
                imagen.width, imagen.height = i.size
            imagen.save()

            data = {'is_valid': True,
                    'documento': imagen.file.name.rsplit('/',1)[1],
                    'url': imagen.file.url,
                    'thumb': imagen.thumb.url
                    }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


#
# Slider
#
class SliderListView(ListView):
    model = Slider
    context_object_name = 'sliders'
    template_name = 'backend/slider_list.html'


class SliderCreateView(CreateView):
    model = Slider
    form_class = SliderForm
    template_name = 'backend/slider_new.html'
    success_message = 'Slider creado correctamente.'
    success_url = reverse_lazy('backend:slider_list')


class SliderEditView(SuccessMessageMixin, UpdateView):
    model = Slider
    form_class = SliderForm
    template_name = 'backend/slider_edit.html'
    success_message = 'Slider editado correctamente.'
    success_url = reverse_lazy('backend:slider_list')


class SliderDeleteView(DeleteView):
    model = Slider
    pk_url_kwarg = 'pk'
    success_message = 'Slider eliminado correctamente.'
    success_url = reverse_lazy('backend:slider_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(SliderDeleteView, self).delete(request, *args, **kwargs)


#
# Grupo Enlace
#
class GrupoEnlaceListView(ListView):
    model = GrupoEnlace
    context_object_name = 'grupoenlaces'
    template_name = 'backend/grupoenlace_list.html'


class GrupoEnlaceCreateView(SuccessMessageMixin, CreateView):
    model = GrupoEnlace
    fields = ['nombre']
    template_name = 'backend/grupoenlace_new.html'
    success_message = 'Enlace creado correctamente.'
    success_url = reverse_lazy('backend:grupoenlace_list')


class GrupoEnlaceEditView(SuccessMessageMixin, UpdateView):
    model = GrupoEnlace
    fields = ['nombre']
    template_name = 'backend/grupoenlace_edit.html'
    success_message = 'Enlace editado correctamente.'
    success_url = reverse_lazy('backend:grupoenlace_list')


class GrupoEnlaceDeleteView(DeleteView):
    model = GrupoEnlace
    pk_url_kwarg = 'pk'
    success_message = 'Enlace eliminado correctamente.'
    success_url = reverse_lazy('backend:grupoenlace_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(GrupoEnlaceDeleteView, self).delete(request, *args, **kwargs)


#
# Enlace
#
class EnlaceListView(ListView):
    model = Enlace
    context_object_name = 'enlaces'
    template_name = 'backend/enlace_list.html'


class EnlaceCreateView(SuccessMessageMixin, CreateView):
    model = Enlace
    fields = ['grupo', 'titulo', 'enlace', 'posicion']
    template_name = 'backend/enlace_new.html'
    success_message = 'Enlace creado correctamente.'
    success_url = reverse_lazy('backend:enlace_list')


class EnlaceEditView(SuccessMessageMixin, UpdateView):
    model = Enlace
    fields = ['grupo', 'titulo', 'enlace', 'posicion']
    template_name = 'backend/enlace_edit.html'
    success_message = 'Enlace editado correctamente.'
    success_url = reverse_lazy('backend:enlace_list')


class EnlaceDeleteView(DeleteView):
    model = Enlace
    pk_url_kwarg = 'pk'
    success_message = 'Enlace eliminado correctamente.'
    success_url = reverse_lazy('backend:enlace_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(EnlaceDeleteView, self).delete(request, *args, **kwargs)


#
# Curso
#
class CursoListView(ListView):
    model = Curso
    context_object_name = 'cursos'
    template_name = 'backend/curso_list.html'


class CursoCreateView(SuccessMessageMixin, CreateView):
    model = Curso
    fields = ['titulo', 'enlace']
    template_name = 'backend/curso_new.html'
    success_message = 'Curso creado correctamente.'
    success_url = reverse_lazy('backend:curso_list')


class CursoEditView(SuccessMessageMixin, UpdateView):
    model = Curso
    fields = ['titulo', 'enlace']
    template_name = 'backend/curso_edit.html'
    success_message = 'Curso editado correctamente.'
    success_url = reverse_lazy('backend:curso_list')


class CursoDeleteView(DeleteView):
    model = Curso
    pk_url_kwarg = 'pk'
    success_message = 'Curso eliminado correctamente.'
    success_url = reverse_lazy('backend:curso_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CursoDeleteView, self).delete(request, *args, **kwargs)


#
# Distribucion
#
class DistribucionListView(ListView):
    model = Distribucion
    context_object_name = 'distribuciones'
    template_name = 'backend/distribucion_list.html'


class DistribucionCreateView(SuccessMessageMixin, CreateView):
    model = Distribucion
    fields = ['titulo', 'mujer', 'hombre', 'posicion']
    template_name = 'backend/distribucion_new.html'
    success_message = 'Distribución creada correctamente.'
    success_url = reverse_lazy('backend:distribucion_list')


class DistribucionEditView(SuccessMessageMixin, UpdateView):
    model = Distribucion
    fields = ['titulo', 'mujer', 'hombre', 'posicion']
    template_name = 'backend/distribucion_edit.html'
    success_message = 'Distribución editada correctamente.'
    success_url = reverse_lazy('backend:distribucion_list')


class DistribucionDeleteView(DeleteView):
    model = Distribucion
    pk_url_kwarg = 'pk'
    success_message = 'Distribución eliminada correctamente.'
    success_url = reverse_lazy('backend:distribucion_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DistribucionDeleteView, self).delete(request, *args, **kwargs)


#
# Dependencia
#
class DependenciaListView(ListView):
    model = Dependencia
    context_object_name = 'dependencias'
    template_name = 'backend/dependencia_list.html'


class DependenciaCreateView(SuccessMessageMixin, CreateView):
    model = Dependencia
    fields = ['nombre', 'direccion', 'ciudad', 'departamento', 'telefono1', 'telefono2', 'email']
    template_name = 'backend/curso_new.html'
    success_message = 'Dependencia creada correctamente.'
    success_url = reverse_lazy('backend:dependencia_list')


class DependenciaEditView(SuccessMessageMixin, UpdateView):
    model = Dependencia
    fields = ['nombre', 'direccion', 'ciudad', 'departamento', 'telefono1', 'telefono2', 'email']
    template_name = 'backend/curso_edit.html'
    success_message = 'Dependencia editada correctamente.'
    success_url = reverse_lazy('backend:dependencia_list')


class DependenciaDeleteView(DeleteView):
    model = Dependencia
    pk_url_kwarg = 'pk'
    success_message = 'Dependencia eliminada correctamente.'
    success_url = reverse_lazy('backend:dependencia_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DependenciaDeleteView, self).delete(request, *args, **kwargs)


#
# Estadistica
#
class EstadisticaListView(ListView):
    model = Estadistica
    context_object_name = 'estadisticas'
    template_name = 'backend/estadistica_list.html'
    ordering = ['-id']


class EstadisticaEditView(SuccessMessageMixin, UpdateView):
    model = Estadistica
    fields = ['descripcion', 'dato', 'icono']
    template_name = 'backend/estadistica_edit.html'
    success_message = 'Estadística editada correctamente.'
    success_url = reverse_lazy('backend:estadistica_list')



