import redis
import vonage

redis_client = redis.Redis()

class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = str(redis_client.get('SECRET_KEY').decode('utf-8'))
    SQLALCHEMY_DATABASE_URI = str(redis_client.get('POSTGRES_URL').decode('utf-8'))

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = False
    SECRET_KEY = str(redis_client.get('SECRET_KEY').decode('utf-8'))
    SQLALCHEMY_DATABASE_URI = str(redis_client.get('POSTGRES_URL').decode('utf-8'))

class TestingConfig(Config):
    TESTING = True


key = str(redis_client.get("VONAGE_KEY").decode("utf-8"))
secret = str(redis_client.get("VONAGE_SECRET").decode("utf-8"))
number = int(redis_client.get("VONAGE_NUMBER").decode("utf-8"))

client = vonage.Client(key=key, secret=secret)
sms = vonage.Sms(client)
