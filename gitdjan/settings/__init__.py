import os

try:
    from local import *
except:
    from production import *


GITS_DIR = os.path.join(BASE_DIR, 'gits')

# Login Page
LOGIN_USERNAME = "0r1gamic"
LOGIN_PASSWORD = "gitdjango123"
LOGIN_URL = '/login'
