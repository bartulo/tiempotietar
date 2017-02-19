from django.conf import settings
 
import twilio
import twilio.rest
import os
 
 
def send_twilio_message(to_number, body):
    client = twilio.rest.TwilioRestClient(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
 
    return client.messages.create(
        body=body,
        to=to_number,
        from_= '986080515'
    )

def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "cuenta_de_%s_a_%s_%s_horas_dia_%s.%s" % (instance.vendedor, instance.comprador, instance.horas, instance.fecha.day, ext)

    return os.path.join(
        'cuentas', str(instance.fecha.year), str(instance.fecha.month), filename
    )

def get_upload_path_articulo(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.nombre, ext)

    return os.path.join(
        'articulos', str(instance.tipo).decode('utf8').encode('ascii', 'ignore'), str(instance.categoria).decode('utf8').encode('ascii', 'ignore'), str(instance.subcategoria).decode('utf8').encode('ascii', 'ignore'), filename
    )
