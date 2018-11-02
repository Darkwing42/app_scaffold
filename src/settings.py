import os

class Config(object):
	DEBUG = False
	CSRF_ENABLED = True
	POSTGRES_USER = os.getenv('POSTGRES_USER')
	POSTGRES_PW = os.getenv('POSTGRES_PASSWORD')
	POSTGRES_URL = "database:5432"
	POSTGRES_DB = os.getenv('POSTGRES_DB')
	SECRET_KEY = os.getenv('SECRET_KEY')
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
	JWT_BLACKLIST_ENABLED = True
	JWT_BLACLIST_TOKEN_CHECKS = ['access', 'refresh']

	# TODO: create secret key func and create secret key at creation if the file
	SQLALCHEMY_DATABASE_URI = DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)


class DevelopmentConfig(Config):
	"""Config for dev"""
	DEBUG = True

class TestingConfig(Config):
	"""Config for testing """

	DEBUG = True
	TESTING = True

	#TODO: change database to testing

class StageingConfig(Config):
	"""Config for stageing"""

	DEBUG = True

class ProductionConfig(Config):
	"""Config for production """

	DEBUG = False
	TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagineConfig,
    'production': ProductionConfig,

	"tasks": {
	"BACKEND_URL" : os.getenv('BACKEND_URL'),
	"BROKER_URL" : os.getenv('BROKER_URL')
	}

}



