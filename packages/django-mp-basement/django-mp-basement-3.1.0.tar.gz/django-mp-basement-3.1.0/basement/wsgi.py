
import cbsettings

from django.core.wsgi import get_wsgi_application


cbsettings.configure('core.settings.Settings')

application = get_wsgi_application()
