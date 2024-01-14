import os
import secrets
import string
from urllib.parse import quote


def urlencode_for_db(s): return quote(str(s), safe='')


def import_temp_env():
    if not os.path.exists('.env'):
        return
    print('[info] Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            key, value = var[0].strip(), var[1].strip()
            os.environ[key] = value


import_temp_env()

# Database settings
DB_HOST = os.getenv(
    'DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'mygpt')
DB_CHARSET = os.getenv('DB_CHARSET', 'utf8')
DB_URL = 'postgres://{username}:{pwd}@{host}:{port}/{dbname}'.format(
    username=urlencode_for_db(DB_USER),
    pwd=urlencode_for_db(DB_PASSWORD),
    host=urlencode_for_db(DB_HOST),
    port=urlencode_for_db(DB_PORT),
    dbname=urlencode_for_db(DB_NAME),
)

# domain
DOMAIN = os.getenv(
    'DOMAIN', '')

GPTBASE_KEY = os.getenv(
    'GPTBASE_KEY', '')

GPTBASE_URL = os.getenv(
    'GPTBASE_URL', '')

WECHAT_TOKEN = os.getenv(
    'WECHAT_TOKEN', '')


WECHAT_KEY = os.getenv(
    'WECHAT_KEY', '')


WECHAT_CORP_ID = os.getenv(
    'WECHAT_CORP_ID', '')

GPTBASE_AI_ID = os.getenv(
    'GPTBASE_AI_ID', '')




# TortoiseORM settings
TORTOISE_ORM = {
    'connections': {
        'default': DB_URL,
    },
    'apps': {
        'models': {
            'models': ['gptbase_enterprise.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}


def api_key() -> str:
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(48))
    return f'ak-{token}'
