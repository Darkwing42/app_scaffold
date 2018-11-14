from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from src.settings import app_config 
from src.db import db
from flask_cors import CORS

def create_app(config_name):

	app = Flask(__name__)
	api = Api(app)
	cors = CORS(app)
	app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
	app.config.from_object(app_config[config_name])
	

	jwt = JWTManager(app)
	
	@jwt.user_claims_loader
	def add_claims_to_jwt(identity):
		from user.models import User
		#TODO: change condition to check if user is admin
		if identity == 1:
			return { 'is_admin': True }
		return { 'is_admin': False }
	
	@jwt.token_in_blacklist_loader
	def check_if_token_in_blacklist(decrypted_token):
		from security.blacklist.models import TokenBlacklist
		
		return decrypted_token['jti'] in TokenBlacklist.get_all()
	
	@jwt.expired_token_loader
	def expired_token_callback():
		return jsonify({
		"description": "The token has expired",
		"error": "token_expired"
		}), 401
	
	@jwt.invalid_token_loader
	def invalid_token_callback(error):
		return jsonify({
		"description": "Signature verification failed",
		"error": "invalid_token"
		}), 401
		
	@jwt.unauthorized_loader
	def missing_token_callback(error):
		return jsonify({
		"description": "Request does not contain an access token",
		"error": "unauthorized_required"
		}), 401
	
	@jwt.needs_fresh_token_loader
	def token_not_fresh_call():
		return jsonify({
		"description": "The token has been revoked",
		"error": "token_revoked"
		}), 401
	


	### resource area ### 
	
	from user.resources import (
								UserRegisterAPI,
								UserLoginAPI,
								UserAPI,
								UserLogoutAPI,
								TokenRefreshAPI
								)
	api.add_resource(UserRegisterAPI, '/api/v1/register')
	api.add_resource(UserLoginAPI, '/api/v1/login')
	api.add_resource(UserLogoutAPI, '/api/v1/logout')
	api.add_resource(TokenRefreshAPI, '/api/v1/refresh')
	api.add_resource(UserApi, '/api/v1/user')


	db.init_app(app)

	return app
