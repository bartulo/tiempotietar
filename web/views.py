from django.shortcuts import render
from web.models import *
from web.forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from web.utils import send_twilio_message
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView

### BUSQUEDA POR PALABRA ###
def busqueda_palabra(request):
  if request.method == 'POST':
    palabra = request.POST['palabra']
    art = Articulo.objects.filter(nombre__icontains = palabra).distinct('nombre')
    return render(request, 'resultado_palabra.html', {'nombre': 'Resultados', 'articulo': art})

def resultado_palabra(request):
  if request.method == 'POST':
    palabra = request.POST['palab']
    art = Articulo.objects.filter(nombre__icontains = palabra)
    return render(request, 'articulo_palabra.html', {'nombre': palabra, 'articulo': art})

def contacto(request):
  return render(request, 'contacto.html')

def novedades(request):
  art = Articulo.objects.order_by('-fecha')[:10]
  return render(request, 'novedades.html', {'arts':art} )

@login_required
def borrarArticulo(request, pk):
  art = Articulo.objects.get(pk = pk)
  art.delete()
  return HttpResponseRedirect('/')
	
@login_required
def nuevoArticulo(request):
  if request.method == 'POST':
    form = ArticuloForm(request.POST)
    if form.is_valid():
      art = form.save(commit=False)
      art.user = request.user
      art.save()
      return HttpResponseRedirect('/')
  else:
    form = ArticuloForm()
    return render(request, 'nuevo_articulo.html', {'form':form} )
  

@login_required
def edit(request):
   # This body will only run if the user is logged in
   # and the current logged in user will be in request.user
   if request.method == 'POST':
        # formulario enviado
     user_form = UserEditForm(request.POST, instance = request.user)
     perfil_form = SocioEditForm(request.POST, instance = request.user.socio)

     if user_form.is_valid() and perfil_form.is_valid():
            # formulario validado correctamente
        user_form.save()
        perfil_form.save()
        return HttpResponseRedirect('/')

   else:
     edit_form = UserEditForm(instance=request.user)
     socio_form = SocioEditForm(instance=request.user.socio)
     return render(request, 'editar.html',
                             {'form':edit_form, 'form_socio':socio_form})

@login_required
def editar_serv(request, num):
   # This body will only run if the user is logged in
   # and the current logged in user will be in request.user
   if request.method == 'POST':
        # formulario enviado
     art = Articulo.objects.get(pk=num)
     art_form = ArticuloForm(request.POST, instance = art)

     if art_form.is_valid():
            # formulario validado correctamente
        art_form.save()
        return HttpResponseRedirect('/')

   else:
     art = Articulo.objects.get(pk=num)
     art_form = ArticuloForm(instance=art)
     return render(request, 'editar_art.html',
                             {'nombre': art.nombre, 'art_form':art_form})

@login_required
def cuentas(request):
  return render(request, 'cuentas.html')

def busqueda(request):
  def filtro(cat):
    res = []
    for i in Articulo.objects.filter(tipo = 'oferta', categoria = cat).distinct('subcategoria'):
      res.append(i.subcategoria)
    return res
  return render(request, 'busqueda.html', {'bienes_comp':filtro('bienes_comp'),'bienes_alq':filtro('bienes_alq'),'clases':filtro('clases'),'servicios':filtro('servicios')})

def busqueda_demandas(request):
  def filtro(cat):
    res = []
    for i in Articulo.objects.filter(tipo = 'demanda', categoria = cat).distinct('subcategoria'):
      res.append(i.subcategoria)
    return res
  return render(request, 'busqueda_demandas.html', {'bienes_comp':filtro('bienes_comp'),'bienes_alq':filtro('bienes_alq'),'clases':filtro('clases'),'servicios':filtro('servicios')})


def resultado(request, cat, subcat):
  if request.method == 'POST':
    articulo = request.POST.get("nombre")
    art = Articulo.objects.filter(nombre = articulo)
    return render(request, 'articulo.html', {'nombre': articulo, 'articulo': art})
  else:
    subc = SubCategoriaArticulo.objects.get(pk = subcat)
    art = Articulo.objects.filter(categoria = cat).filter(subcategoria = subc).filter(activo = True).distinct('nombre')
    return render(request, 'resultado.html', {'cat': art[0].get_categoria_display().upper(), 'subcat': subc.nombre, 'articulo': art})

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, uidb64=uidb64, token=token, post_reset_redirect=reverse('login'))


def reset(request):
    return password_reset(request, post_reset_redirect=reverse('login')) 

# SMS ############

@twilio_view
def sms(request):
  body = request.POST.get('Body','')
  reg = RegistroSMS.objects.get(pk=body)
  msg = "Hola %s, que tal %s" % (reg.comprador.first_name, reg.vendedor.username)
  r = Response()
  r.sms(msg)
  return r

#### REGISTRO POR SMS ####

class registroSmsCreateView(CreateView):
  model = RegistroSMS
  form_class = RegistroSmsForm
  template_name = 'registro_sms.html'
  success_url = reverse_lazy('registro_sms')

  def form_valid(self, form):
    formulario = form.save(commit=False)
    usuario = self.request.user
    formulario.comprador = usuario
    salvado = form.save()
    sent = send_twilio_message(usuario.socio.telefono, 'probando %s' % salvado.pk)
