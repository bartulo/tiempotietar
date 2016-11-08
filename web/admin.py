# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.admin.helpers import ActionForm
from django.http import HttpResponse
from django import forms
from web.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

#### Clase para ordenar el filtro vendedor de la página de cuentas 

class VendedorFilter(SimpleListFilter):
  title = _('Vendedor')

  parameter_name = 'vendedor'

  def lookups(self, request, model_admin):
    qs = model_admin.get_queryset(request)
    return [(i, User.objects.get(pk=i)) for i in qs.values_list('vendedor', flat=True).distinct().order_by('vendedor')]

  def queryset(self, request, queryset):
    if self.value():
      return queryset.filter(vendedor__exact=self.value())

#### Clase para ordenar el filtro comprador de la página de cuentas 

class CompradorFilter(SimpleListFilter):
  title = _('Comprador')

  parameter_name = 'comprador'

  def lookups(self, request, model_admin):
    qs = model_admin.get_queryset(request)
    return [(i, User.objects.get(pk=i)) for i in qs.values_list('comprador', flat=True).distinct().order_by('comprador')]

  def queryset(self, request, queryset):
    if self.value():
      return queryset.filter(comprador=self.value())

def exportar_csv_cuentas(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=cuentas.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"horas"),
        smart_str(u"vendedor"),
        smart_str(u"comprador"),
        smart_str(u"fecha"),
    ])
    for obj in queryset:
      writer.writerow([
            smart_str(obj.horas),
            smart_str(obj.vendedor),
            smart_str(obj.comprador),
            smart_str(obj.fecha),
      ])
    return response
exportar_csv_cuentas.short_description = u"Exportar CSV"

#### Página de Cuentas en Admin 

class CuentaAdmin(admin.ModelAdmin):
  list_display = ('horas', 'vendedor', 'comprador', 'fecha',)
  list_filter = ['fecha', VendedorFilter, CompradorFilter] 
  actions = [exportar_csv_cuentas]

#### 

class UpdateActionForm(ActionForm):
  subcategoria = forms.CharField(required=False)

def cambiar_subcat(modeladmin, request, queryset):
  sc = request.POST['subcategoria']
  try:
    subcat = SubCategoriaArticulo.objects.get(nombre = sc)
    queryset.update(subcategoria=subcat)
  except:
    modeladmin.message_user(request, 'Subcategoria no válida')

class ArticuloAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'user', 'tipo', 'categoria', 'subcategoria', 'fecha')
  list_filter = ['fecha', 'tipo', 'categoria', 'subcategoria', 'user'] 
  action_form = UpdateActionForm
  actions = [cambiar_subcat]
  list_per_page = 200

class SocioInline(admin.StackedInline):
  model = Socio

def exportar_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=socio.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Num_Socio"),
        smart_str(u"Nombre"),
        smart_str(u"e-mail"),
    ])
    for obj in queryset:
      if obj.is_active:
        try:
          writer.writerow([
            smart_str(obj.username),
            smart_str(obj.first_name + " " + obj.last_name),
            smart_str(obj.email),
            smart_str(obj.socio.pueblo),
            smart_str(obj.socio.telefono),
          ])
        except:
          pass
    return response
exportar_csv.short_description = u"Exportar CSV"

class UserAdmin(UserAdmin):
  inlines = (SocioInline, )
  list_display = ('socio', 'first_name', 'last_name', 'horas_positivas', 'horas_negativas', 'horas_totales', )
  list_per_page = 500
  actions = [exportar_csv]

  def num_user(self, obj):
      return obj.socio.numsocio
  num_user.short_description = 'Numero de socio'

  def horas_positivas(self, obj):
    total = 0  
    for i in obj.vendedor.all():
      total = total + i.horas
    for n in obj.adminind_set.all():
      total = total + n.horas
    return "%.2f" % total
  horas_positivas.short_description = 'Horas Positivas'

  def horas_negativas(self, obj):
    total = 0  
    for n in obj.admin_set.all():
      total = total + sum([r.horas for r in n.adminind_set.all()])/n.user.count()
    for i in obj.comprador.all():
      total = total + i.horas 
    return "%.2f" % total 
  horas_negativas.short_description = 'Horas Negativas'

  def horas_totales(self, obj):
    return float(self.horas_positivas(obj)) - float(self.horas_negativas(obj)) 

class AdminIndInLine(admin.TabularInline):
  model = AdminInd

class AdminAdmin(admin.ModelAdmin):
  list_display = ('__unicode__', 'fecha', )
  list_filter = ['fecha']
  exclude = ('user', )
  inlines = [
      AdminIndInLine,
  ]

  def save_model(self,request, obj, form, change):
    obj.save()
    for i in User.objects.filter(is_active=True):
      obj.user.add(i)

admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(SubCategoriaArticulo)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Admin, AdminAdmin)
