from django.conf.urls import patterns, url

from web import views

urlpatterns = patterns('',
    url(r'^cuentas/', views.cuentas, name='cuentas'),
    url(r'^contacto/', views.contacto, name='contacto'),
    url(r'^busqueda/', views.busqueda, name='busqueda'),
    url(r'^busquedaPalabra/', views.busqueda_palabra, name='busqueda_palabra'),
    url(r'^resultadoPalabra/', views.resultado_palabra, name='resultado_palabra'),
    url(r'^editar/(?P<num>\d+)', views.editar_serv, name='editar_serv'),
    url(r'^editar/', views.edit, name='editar'),
    url(r'^novedades/', views.novedades, name='novedades'),
    url(r'^nuevoArticulo/', views.nuevoArticulo, name='nuevo_articulo'),
    url(r'^borrarArticulo/(?P<pk>\d+)', views.borrarArticulo, name='borrar_articulo'),
    url(r'^resultado/(?P<cat>\w+)/(?P<subcat>\d+)', views.resultado, name='resultado'),
    url(r'^sms/$', views.sms),
    url(r'^registro/$', views.registroSmsCreateView.as_view(), name='registro_sms'),
)
