from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm


from backend.models import *


def index(request):
    estadisticas = Estadistica.objects.all()
    galerias = Galeria.objects.filter(activa=True, recomendada=True)
    sliders = Slider.objects.filter(activa=True)
    categoria_noticia = Categoria.objects.get(slug__exact='noticias').get_descendants(include_self=True)
    noticias = Contenido.objects.filter(categoria__in=categoria_noticia, activo=True, recomendado=True).order_by('id')
    categoria_estadistica = Categoria.objects.get(slug__exact='estadisticas').get_descendants(include_self=True)
    contenido_estadisticas = Contenido.objects.filter(categoria__in=categoria_estadistica).order_by('id')[:4]
    distribuciones = Distribucion.objects.all()
    cursos = Curso.objects.all()

    ctx = {'estadisticas': estadisticas,
           'galerias': galerias,
           'sliders':sliders,
           'noticias': noticias,
           'contenido_estadisticas': contenido_estadisticas,
           'distribuciones': distribuciones,
           'cursos': cursos }
    return render(request, 'basew.html', ctx)


class ContenidoListView(ListView):
    model = Contenido
    context_object_name = 'contenidos'
    template_name = 'www/contenido_list.html'

    def get_queryset(self):
        self.categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return Contenido.objects.filter(categoria=self.categoria)


def contenido_list(request, slug, slug2=None, slug3=None):
    if slug3:
        categoria = get_object_or_404(Categoria, slug=slug3)
    elif slug2:
        categoria = get_object_or_404(Categoria, slug=slug2)
    elif slug:
        categoria = get_object_or_404(Categoria, slug=slug)

    contenidos = Contenido.objects.filter(categoria__exact=categoria)
    ctx = {'categoria': categoria,
           'breadcrumbs': categoria.get_ancestors(ascending=False, include_self=True),
           'contenidos': contenidos,
           }
    return render(request, 'www/contenido_list.html', ctx)


def contenido_detail(request, slug):
    contenido = get_object_or_404(Contenido, slug=slug)
    categorias = contenido.categoria.get_ancestors(ascending=False, include_self=True)

    ultimos = Contenido.objects.filter(categoria__in=categorias).exclude(id=contenido.id)[:5]
    print(ultimos)

    ctx = {
           'breadcrumbs': categorias,
           'contenido': contenido,
           'noimage': "/media/imagenes/no-image" in contenido.imagen.url,
           'ultimos': ultimos
           }
    return render(request, 'www/contenido_detail.html', ctx)


class GaleriaListView(ListView):
    model = Galeria
    context_object_name = 'galerias'
    template_name = 'www/galeria_list.html'
    queryset = Galeria.objects.all().order_by('-creada')


class GaleriaDetailView(DetailView):
    model = Galeria
    template_name = 'www/galeria_detail.html'


def galeria_detail(request, slug):
    object = get_object_or_404(Galeria, slug=slug)
    #categoria = contenido.categoria
    galerias = Galeria.objects.all()[:5]
    print(object)

    ctx = {'galerias': galerias,
           'object': object

           }
    return render(request, 'www/galeria_detail.html', ctx)


class DependenciaListView(ListView):
    model = Dependencia
    context_object_name = 'dependencias'
    template_name = 'www/dependencia_list.html'
    queryset = Dependencia.objects.all()


