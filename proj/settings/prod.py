from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'budget.2nfjvnb9vu.ap-northeast-2.elasticbeanstalk.com'
]

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS':{
                'read_default_file':'.config/my.cnf'
            }
        }
    }