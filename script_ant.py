from django.contrib.auth.models import User
from web.models import * 
import psycopg2
import datetime

def add_user():
  for i in open('socios.csv', 'r'):
    w = i.split(",")
    if w[1] != "" and int(w[0]) > 0:
      user = User.objects.create_user(w[0], w[4], w[0])
      user.first_name = w[1]
      user.last_name = w[2]
      user.save()
    if int(w[0]) < 0 and w[1] != "":
      user = User.objects.create_user(-int(w[0]), w[4], w[0])
      user.first_name = w[1]
      user.last_name = w[2]
      user.is_active = False
      user.save()

def mod_user():
  for i in open('socios.csv', 'r'):
    w = i.split(",")
    if w[1] != "" and int(w[0]) > 0:
      a = User.objects.get(username=w[0])
      s = Socio(user=a, telefono=w[3], pueblo=w[6], numsocio=int(w[0]))
      s.save()
    if w[1] != "" and int(w[0]) < 0:
      a = User.objects.get(username=-int(w[0]))
      s = Socio(user=a, telefono=w[3], pueblo=w[6], numsocio=-int(w[0]))
      s.save()

def add_art():
  c = SubCategoriaArticulo.objects.get(nombre='Otros')
  categoria = [(8, 'servicios'),(9, 'clases'),(10, 'bienes_alq'),(11, 'bienes_comp')]

  for cat in categoria:
    for i in open('socios_corregido.csv', 'r'):
      w = i.split(",")
      f = w[12].split("-")
      if w[cat[0]] != "" and int(w[0]) > 0:
        fecha = datetime.date(int(f[0]), int(f[1]), int(f[2])) 
        user = User.objects.get(username = w[0])
        art = Articulo(user = user, tipo = 'oferta', categoria = cat[1], subcategoria = c, nombre = w[cat[0]], fecha = fecha)
        art.save()

def a(num):
  conn = psycopg2.connect("dbname=temp")
  cur = conn.cursor()
  for i in open("csv/horas%i.csv" % (num), "r"):
    w = i.split(",")
    f = w[2].split("-")
    fecha = datetime.date(int(f[0]), int(f[1]), int(f[2])) 
    cur.execute("select * from horas where fecha = %s and horas = %s", (fecha, -float(w[1])))
    neg = cur.fetchall()
    cur.execute("select * from horas where fecha = %s and horas = %s", (fecha, float(w[1])))
    pos = cur.fetchall()
    l1 = [n[2] for n in pos]
    l2 = [n[2] for n in neg]
    while l1.__len__() > 0:
      pares = []
      if l1 != [n for n in l1 if n == l1[0]]:
        if l1[0] != l1[1]:
          try:
            t = l2.index(l1[1])
          except:
            t = 0
        else:
            t = 0
      else:
        t = 0
      pares.append(l1.pop(0))
      pares.append(l2.pop(t))  
      vend = User.objects.get(username = pares[0])
      comp = User.objects.get(username = pares[1])
      art = vend.articulo_set.all()
      if art.count() == 0:
        c = SubCategoriaArticulo.objects.get(nombre='Otros')
        art_null = Articulo(user=vend, tipo='oferta', categoria='clases', subcategoria=c, nombre='null')
        art_null.save()
      cuenta = Cuenta(vendedor=vend, comprador=comp, fecha=pos[0][1], horas=pos[0][0], articulo= art[0])
      print pares, pos[0][1], art[0], pos[0][0]   
      cuenta.save()

def e():
  w = open('csv/cuentas.csv', 'w')
  for i in Cuenta.objects.all():
    w.write(str(i.horas) + ',' + i.vendedor.username + ',' + i.comprador.username + ',' + str(i.fecha) + '\n')
  w.close()

def b():
  for i in open("csv/cuentas.csv", "r"):
    w = i.split(",")
    f = w[3].split("-")
    fecha = datetime.date(int(f[0]), int(f[1]), int(f[2])) 
    vend = User.objects.get(username = w[1])
    comp = User.objects.get(username = w[2])
    art = vend.articulo_set.all()
    if art.count() == 0:
      c = SubCategoriaArticulo.objects.get(nombre='Otros')
      art_null = Articulo(user=vend, tipo='oferta', categoria='clases', subcategoria=c, nombre='null', fecha = datetime.date.today())
      art_null.save()
    cuenta = Cuenta(vendedor=vend, comprador=comp, fecha=fecha, horas=w[0], articulo= art[0])
    cuenta.save()

def administradores():
  conn = psycopg2.connect("dbname=temp")
  cur = conn.cursor()
  for i in open("csv/administradores.csv", "r"):
    w = i.split(",")
    f = w[2].split("-")
    fecha = datetime.date(int(f[0]), int(f[1]), int(f[2])) 
    cur.execute("select * from horas where fecha = %s and horas = %s", (fecha, w[1]))
    datos = cur.fetchall()
    try:
      admini = Admin.objects.get(fecha=fecha)
    except:
      admini = Admin.objects.create(fecha=fecha)
    for n in datos:
      trador = User.objects.get(username = n[2])
      ind = AdminInd(administrador=trador, horas=n[0], entrada=admini)
      ind.save()
    cur.execute("select * from neg where fecha = %r and cuenta > 20;" % (str(fecha)))
    datos2 = cur.fetchone()
    cur.execute("select * from horas where fecha = %r and horas = %s" % (str(fecha), datos2[1]))
    datos3 = cur.fetchall()
    for r in datos3:
      u = User.objects.get(username=abs(r[2]))
      admini.user.add(u)
