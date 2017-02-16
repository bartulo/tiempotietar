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
    filename = "cuenta_%s.%s" % (instance.id, ext)

    return os.path.join(
        'cuentas', str(instance.fecha.year), str(instance.fecha.month), filename
    )
