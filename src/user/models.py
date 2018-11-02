from src.db import BaseModel as db 
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid_converter import str2uuid
import bcrypt
import uuid
from marshmallow import fields, Schema



class UserSettings(db.Model):
	__tablename__ = 'usersettings'

	userSettingsID = db.Column(db.Integer, primary_key=True)
	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)

	created_at = db.Column(db.Datetime, default=datetime.datetime.now)
	modified_at = db.Column(db.Datetime, default=datetime.datetime.now)


	def json(self):
		return dict(
				id=str(self.id),
				created_at=self.created_at.strftime('%d-%m-%Y %H:%M'),
				modified_at=self.modified_at.strftime('%d-%m-%Y %H:%M')
				)

class UserSettingsSchema(Schema):
	id = fields.Str(dump_only=True)
    
	
	created_at = fields.DateTime(dump_only=True)
	modified = fields.DateTime(dump_only=True)


class User(db.Model):
	__tablename__ = 'users'

	userID = db.Column(db.Integer, primary_key=True)
	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	kuerzel=db.Column(db.String(10))
	email = db.Column(db.String, nullable=False, unique=True)
	is_admin = db.Column(db.Boolean, default=False)
	authenticated = db.Column(db.Boolean, default=False)
	is_active = db.Column(db.Boolean, default=True)

	settings = db.relationship('UserSettings', backref='User', lazy=False)
	
	_password = db.Column(db.Binary(60), nullable=False)

	created_at = db.Column(db.Datetime, default=datetime.datetime.now)
	modified_at = db.Column(db.Datetime, default=datetime.datetime.now)


	def __init__(self, username, password, email):
		self.username = username
		self._password = self._hash_password(password).encode('utf-8')
		self.email = email
		self.authenticated = False

	def _hash_password(plain_password):
		return bcrypt.hashpw(plain_password, bycrypt.gensalt(12))

	def check_password(user_pw, hashed_pw):
		return bcrypt.checkpw(user_pw, hashed_pw)

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()
	

	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id=(str2uuid(id))).first()
	

	def json(self):
		return dict(
				id=str(self.id),
				username=self.username,
				kuerzel=self.kuerzel,
				email=self.email,
				settings=[ setting.json() for setting in self.settings ],
				created_at=self.created_at.strftime('%d-%m-%Y %H:%M'),
				modified_at=self.modified_at.strftime('%d-%m-%Y %H:%M')
				
				)
	
class UserSchema(Schema):
	id = fields.Str(dump_only=True)
	username = fields.Str(required=True)
	email = fields.Email(required=True)
	password = fields.Str(required=True)

	created_at = fields.DateTime(dump_only=True)
	modified = fields.DateTime(dump_only=True)

	settings = fields.Nested(UserSettingsSchema, many=True)
