from .base import *

if on_heroku:
    from .production import *
else:
    from .local import *
