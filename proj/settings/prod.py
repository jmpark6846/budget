from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'budget.2nfjvnb9vu.ap-northeast-2.elasticbeanstalk.com'
]

print('RDS_HOSTNAME' in os.environ)
print(os.environ)


if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }



