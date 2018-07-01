from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

app_name = 'www'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^glosario/$', TemplateView.as_view(template_name="www/glosario.html"), name='glosario'),
    url(r'^agenda/$', TemplateView.as_view(template_name="www/agenda.html"), name='agenda'),
    url(r'^mapa-iberoamerica/$', TemplateView.as_view(template_name="www/mapa-iberoamerica.html"),
        name='mapa_iberoamerica'),
    url(r'^quienes-somos/$', TemplateView.as_view(template_name="www/quienes_somos.html"), name='quienes_somos'),
    url(r'^quienes-somos/observatorio/$', TemplateView.as_view(template_name="www/observatorio.html"),
        name='observatorio'),
    url(r'^quienes-somos/mision-vision/$', TemplateView.as_view(template_name="www/mision.html"), name='mision'),
    url(r'^quienes-somos/objetivos/$', TemplateView.as_view(template_name="www/objetivos.html"), name='objetivos'),
    url(r'^marco-normativo/nacional/constitucion-nacional$',
        TemplateView.as_view(template_name="www/constitucion_nacional.html"), name='constitucion_nacional'),
    url(r'^dependencia/$', views.DependenciaListView.as_view(), name='dependencia_list'),
    url(r'^galeria/$', views.GaleriaListView.as_view(), name='galeria_list'),
    url(r'^galeria/(?P<slug>[-\w]+)/$', views.galeria_detail, name='galeria_detail'),
    url(r'^contenido/(?P<slug>[-\w]+)$', views.contenido_detail, name='contenido_detail'),
    url(r'^(?P<slug>[-\w]+)/$', views.contenido_list),
    url(r'^(?P<slug>[-\w]+)(?:/(?P<slug2>[-\w]+))(?:/(?P<slug3>[-\w]+))?/$', views.contenido_list),
    # url(r'^galeria/new/$', views.GaleriaCreateView.as_view(), name='galeria_new'),
    # url(r'^galeria/(?P<pk>\d+)/delete/$', views.GaleriaDeleteView.as_view(), name='galeria_delete'),
    # url(r'^galeria/(?P<pk>\d+)/imagen-upload/$', views.ImagenUploadView.as_view(), name='foto_upload'),
    # url(r'^imagen/(?P<pk>\d+)/delete/$', views.imagen_delete, name='imagen_delete'),
    # url(r'^ajax/load-subcategorias/$', views.categoria_leaf_node, name='ajax_load_subcategoria'),
    # url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
    # url(r'^slider/$', views.SliderListView.as_view(), name='slider_list'),
    # url(r'^slider/new/$', views.SliderCreateView.as_view(), name='slider_new'),
    # url(r'^slider/(?P<pk>\d+)/edit/$', views.SliderEditView.as_view(), name='slider_edit'),
    # url(r'^slider/(?P<pk>\d+)/delete/$', views.SliderDeleteView.as_view(), name='slider_delete'),


    # url(r'^persona/$', views.persona_list, name='persona_list'),
    # url(r'^persona/(?P<user_id>[0-9]+)/$', views.persona_edit, name='persona_edit'),
    # url(r'^persona/(?P<user_id>[0-9]+)/delete/$', views.PersonaDelete.as_view(), name='persona_delete'),
    # url(r'^persona/add/$', views.persona_add, name='persona_add'),
    # url(r'^votante/$', views.votante_list, name='votante_list'),
    # url(r'^votante/add/$', views.votante_add, name='votante_add'),
]
