from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


from backend.models import *


def index(request):
    estadisticas = Estadistica.objects.all().order_by('id')
    galerias = Galeria.objects.filter(activa=True, recomendada=True)
    sliders = Slider.objects.filter(activa=True)
    categoria_noticia = Categoria.objects.get(slug__exact='noticias').get_descendants(include_self=True)
    noticias = Contenido.objects.filter(categoria__in=categoria_noticia,
                                        activo=True,
                                        recomendado=True,
                                        fecha_publicacion__lte=datetime.now()).order_by('id')
    categoria_estadistica = Categoria.objects.get(slug__exact='estadisticas').get_descendants(include_self=True)
    contenido_estadisticas = Contenido.objects.filter(categoria__in=categoria_estadistica).order_by('-id')[:4]
    distribuciones = Distribucion.objects.all()
    cursos = Curso.objects.all()

    ctx = {
        'estadisticas': estadisticas,
        'galerias': galerias,
        'sliders': sliders,
        'noticias': noticias,
        'contenido_estadisticas': contenido_estadisticas,
        'distribuciones': distribuciones,
        'cursos': cursos
    }
    return render(request, 'basew.html', ctx)


def contenido_list(request, slug, slug2=None, slug3=None):
    if slug3:
        categoria = get_object_or_404(Categoria, slug=slug3)
    elif slug2:
        categoria = get_object_or_404(Categoria, slug=slug2)
    elif slug:
        categoria = get_object_or_404(Categoria, slug=slug)

    contenidos_list = Contenido.objects.filter(categoria__exact=categoria, activo=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(contenidos_list, 5)
    try:
        contenidos = paginator.page(page)
    except PageNotAnInteger:
        contenidos = paginator.page(1)
    except EmptyPage:
        contenidos = paginator.page(paginator.num_pages)

    ctx = {
        'categoria': categoria,
        'breadcrumbs': categoria.get_ancestors(ascending=False, include_self=True),
        'contenidos': contenidos,
    }
    return render(request, 'www/contenido_list.html', ctx)


def contenido_detail(request, slug):
    contenido = get_object_or_404(Contenido, slug=slug)
    categorias = contenido.categoria.get_ancestors(ascending=False, include_self=True)
    ultimos = Contenido.objects.filter(categoria__in=categorias).exclude(id=contenido.id)[:5]

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
    paginate_by = 3


def galeria_detail(request, slug):
    galeria = get_object_or_404(Galeria, slug=slug)
    galerias = Galeria.objects.all()[:5]

    ctx = {
        'galerias': galerias,
        'object': galeria
    }
    return render(request, 'www/galeria_detail.html', ctx)


class DependenciaListView(ListView):
    model = Dependencia
    context_object_name = 'dependencias'
    template_name = 'www/dependencia_list.html'
    queryset = Dependencia.objects.all()

