from django.contrib.auth.models import User
from web.models import *

with open('s.csv') as f:
   for i in f.readlines():
     s = i.split(';')
     a = User(username = s[0], password = int(s[0]), first_name = s[1], last_name = s[2], email = s[4])
     a.set_password(s[0])
     a.save()
     b = Socio(user = a, numsocio = s[0], telefono = s[3], pueblo = s[6])
     b.save()
