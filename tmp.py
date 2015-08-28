import datetime
from django.contrib.auth.models import *
from web.models import *

def form(fecha):
  f = fecha.split('-')
  return datetime.date(int(f[0]),int(f[1]),int(f[2]))

with open('admin.csv') as f:
   for i in f.readlines():
     s = i.split(',')
     try:
       obj = Admin.objects.get(fecha = form(s[1]))
     except: 
       obj = Admin(fecha = form(s[1]))
       obj.save()
     u = User.objects.get(username = s[2].replace('\n',''))
     c = AdminInd(administrador = u, horas = s[0], entrada = obj)
     c.save()

