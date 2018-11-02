from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from src.settings import app_config 
from src.db import db

def create_app(config_name):

	app = Flask(__name__)
	api = Api(app)
	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	app.config.from_object(app_config[config_name])
	

	jwt = JWTManager(app)



	### resource area ### 


	db.init_app(app)

	return app
