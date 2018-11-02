import bcrypt
from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
		create_access_token,
		create_refresh_token,
		jwt_refresh_token_required,
		get_jwt_identity,
		jwt_required,
		get_raw_jwt
		)
from src.security.blacklist.models import TokenBlacklist
from src.user.models import User, UserSettings

class UserRegisterAPI(Resource):
	def post(self):
		data = request.get_json()

		if User.find_by_username(data['username']):
			return {"message": "A user with this username already exists"}, 400

		if not User.query.all():
			user = User(**data)
			user.is_admin = True
			user.save()
			return {"message": "Admin successfully created"}, 201
		else:
			user = User(**data)
			user.is_admin = False
			user.save()
			return {"message": "User successfully created"}, 201

class UserAPI(Resource):
	
	@jwt_required
	def get(self):
		user = User.find_by_id(get_jwt_identity())

		if not user:
			return {"message": "User not found"}, 404
		return user.json()

class UserLoginAPI(Resource):

	@classmethod
	def post(cls):
		data = request.get_json()
		user = User.find_by_username(data.get('username'))
		if user and user.check_password(data.get('password'), user._password):
			access_token = create_access_token(identity=str(user.id), fresh=True),
			refresh_token = create_refresh_token(identity=str(user.id))
			return {
					"access_token": access_token,
					"refresh_token": refresh_token
					}, 200
		return {"message": "Invalid credentials"},401

class UserLogoutAPI(Resource):
	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']
		token = TokenBlacklist(jti=jti)
		token.save()
		return {"message": "Successfully logged out"}, 200

class TokenRefreshAPI(Resource):
	@jwt_refresh_token_required
	def post(self):
		current_user = get_jwt_identity()
		new_token = create_access_token(identity=current_user, fresh=False)
		return { "access_token" : new_token},200
	
