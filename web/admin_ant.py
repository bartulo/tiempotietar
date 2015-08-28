from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from web.models import *

class CuentaAdmin(admin.ModelAdmin):
  list_display = ('horas', 'vendedor', 'comprador', 'fecha')
  list_filter = ['fecha'] 

class ArticuloAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'user', 'tipo', 'categoria', 'subcategoria', 'fecha')
  list_filter = ['fecha', 'tipo', 'categoria', 'subcategoria'] 

class SocioInline(admin.StackedInline):
  model = Socio

class UserAdmin(UserAdmin):
  inlines = (SocioInline, )
  list_display = ('username', 'horas_positivas', 'horas_negativas', )

  def horas_positivas(self, obj):
    total = 0  
    for i in obj.vendedor.all():
      total = total + i.horas
    return total
  horas_positivas.short_description = 'Horas Positivas'

  def horas_negativas(self, obj):
    total = 0  
    for i in obj.comprador.all():
      total = total + i.horas
    return total
  horas_negativas.short_description = 'Horas Negativas'

admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(SubCategoriaArticulo)
admin.site.register(Cuenta, CuentaAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
