"""Settings for the prodiction (heroku)"""

#Import settings.
from Synergo.settings import *

ALLOWED_HOSTS = ["synergo2.herokuapp.com"]

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
