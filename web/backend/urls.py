from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


from . import views

app_name = 'backend'
urlpatterns = [
    url(r'^$', login_required(TemplateView.as_view(template_name="backend/index.html")), name='index'),

    url(r'^contenido/$', login_required(views.ContenidoListView.as_view()), name='contenido_list'),
    url(r'^contenido/new/$', views.contenido_new, name='contenido_new'),
    url(r'^contenido/(?P<pk>\d+)/edit/$', views.ContenidoEditView.as_view(), name='contenido_edit'),
    url(r'^contenido/(?P<pk>\d+)/delete/$', login_required(views.ContenidoDeleteView.as_view()),
        name='contenido_delete'),

    url(r'^galeria/$', login_required(views.GaleriaListView.as_view()), name='galeria_list'),
    url(r'^galeria/new/$', login_required(views.GaleriaCreateView.as_view()), name='galeria_new'),
    url(r'^galeria/(?P<pk>\d+)/edit/$', views.galeria_edit, name='galeria_edit'),
    url(r'^galeria/(?P<pk>\d+)/delete/$', login_required(views.GaleriaDeleteView.as_view()), name='galeria_delete'),
    url(r'^galeria/(?P<pk>\d+)/imagen-upload/$', views.ImagenUploadView.as_view(), name='foto_upload'),
    url(r'^imagen/(?P<pk>\d+)/delete/$', views.imagen_delete, name='imagen_delete'),
    url(r'^ajax/load-subcategorias/$', views.categoria_leaf_node, name='ajax_load_subcategoria'),
    url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),

    url(r'^slider/$', login_required(views.SliderListView.as_view()), name='slider_list'),
    url(r'^slider/new/$', login_required(views.SliderCreateView.as_view()), name='slider_new'),
    url(r'^slider/(?P<pk>\d+)/edit/$', login_required(views.SliderEditView.as_view()), name='slider_edit'),
    url(r'^slider/(?P<pk>\d+)/delete/$', login_required(views.SliderDeleteView.as_view()), name='slider_delete'),

    url(r'^enlace/$', login_required(views.EnlaceListView.as_view()), name='enlace_list'),
    url(r'^enlace/new/$', login_required(views.EnlaceCreateView.as_view()), name='enlace_new'),
    url(r'^enlace/(?P<pk>\d+)/edit/$', login_required(views.EnlaceEditView.as_view()), name='enlace_edit'),
    url(r'^enlace/(?P<pk>\d+)/delete/$', login_required(views.EnlaceDeleteView.as_view()), name='enlace_delete'),

    url(r'^grupoenlace/$', login_required(views.GrupoEnlaceListView.as_view()), name='grupoenlace_list'),
    url(r'^grupoenlace/new/$', login_required(views.GrupoEnlaceCreateView.as_view()), name='grupoenlace_new'),
    url(r'^grupoenlace/(?P<pk>\d+)/edit/$', login_required(views.GrupoEnlaceEditView.as_view()),
        name='grupoenlace_edit'),
    url(r'^grupoenlace/(?P<pk>\d+)/delete/$', login_required(views.GrupoEnlaceDeleteView.as_view()),
        name='grupoenlace_delete'),

    url(r'^curso/$', login_required(views.CursoListView.as_view()), name='curso_list'),
    url(r'^curso/new/$', login_required(views.CursoCreateView.as_view()), name='curso_new'),
    url(r'^curso/(?P<pk>\d+)/edit/$', login_required(views.CursoEditView.as_view()), name='curso_edit'),
    url(r'^curso/(?P<pk>\d+)/delete/$', login_required(views.CursoDeleteView.as_view()), name='curso_delete'),

    url(r'^distribucion/$', login_required(views.DistribucionListView.as_view()), name='distribucion_list'),
    url(r'^distribucion/new/$', login_required(views.DistribucionCreateView.as_view()), name='distribucion_new'),
    url(r'^distribucion/(?P<pk>\d+)/edit/$', login_required(views.DistribucionEditView.as_view()),
        name='distribucion_edit'),
    url(r'^distribucion/(?P<pk>\d+)/delete/$', login_required(views.DistribucionDeleteView.as_view()),
        name='distribucion_delete'),

    url(r'^dependencia/$', login_required(views.DependenciaListView.as_view()), name='dependencia_list'),
    url(r'^dependencia/new/$', login_required(views.DependenciaCreateView.as_view()), name='dependencia_new'),
    url(r'^dependencia/(?P<pk>\d+)/edit/$', login_required(views.DependenciaEditView.as_view()),
        name='dependencia_edit'),
    url(r'^dependencia/(?P<pk>\d+)/delete/$', login_required(views.DependenciaDeleteView.as_view()),
        name='dependencia_delete'),

    url(r'^estadistica/$', login_required(views.EstadisticaListView.as_view()), name='estadistica_list'),
    url(r'^estadistica/(?P<pk>\d+)/edit/$', login_required(views.EstadisticaEditView.as_view()),
        name='estadistica_edit'),

    #url(r'^curso/$', login_required(views.CursoListView.as_view()), name='curso_list'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', )

    # url(r'^persona/$', views.persona_list, name='persona_list'),
    # url(r'^persona/(?P<user_id>[0-9]+)/$', views.persona_edit, name='persona_edit'),
    # url(r'^persona/(?P<user_id>[0-9]+)/delete/$', views.PersonaDelete.as_view(), name='persona_delete'),
    # url(r'^persona/add/$', views.persona_add, name='persona_add'),
    # url(r'^votante/$', views.votante_list, name='votante_list'),
    # url(r'^votante/add/$', views.votante_add, name='votante_add'),
]
