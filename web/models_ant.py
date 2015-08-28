from django.db import models
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey

class Socio(models.Model):
  user = models.OneToOneField(User)
  numsocio = models.IntegerField()
  pueblo = models.CharField(max_length=200, blank=True)
  telefono = models.CharField(max_length=32, blank=True)
  esta_activo = models.BooleanField(default=True)
  avatar = models.ImageField(upload_to='/home/servidor/tiempodata/avatar/', blank=True)

class SubCategoriaArticulo(models.Model):
  nombre = models.CharField(max_length=100)
  def __unicode__(self):
    return self.nombre

class Articulo(models.Model):
  user = models.ForeignKey(User)
  tipo = models.CharField(max_length=12, choices=(
      ('oferta', 'Oferta'),
      ('demanda', 'Demanda'),
    )
  )
  categoria = models.CharField(max_length=30, choices = (
      ('bienes_alq', 'Bienes Alquiler'),
      ('bienes_comp', 'Bienes Compra'),
      ('clases', 'Clases'),
      ('servicios', 'Servicios')
    )
  )
  subcategoria = models.ForeignKey(SubCategoriaArticulo)
  nombre = models.CharField(max_length=100) 
  descripcion = models.CharField(max_length=300, blank=True)
  foto = models.ImageField(upload_to='/home/servidor/tiempodata/articulo/', blank=True)
  fecha = models.DateField(auto_now=True)
  def __unicode__(self):
    return self.nombre

class Cuenta(models.Model):
  vendedor = models.ForeignKey(User, related_name='vendedor')
  comprador = models.ForeignKey(User, related_name='comprador')
  horas = models.FloatField()
  articulo = ChainedForeignKey(Articulo, chained_field="vendedor", chained_model_field="user", auto_choose=True)
  fecha = models.DateField(auto_now_add=True)
  
  def __unicode__(self):
    return '%s horas de %s a %s'% (self.horas, self.comprador, self.vendedor)

