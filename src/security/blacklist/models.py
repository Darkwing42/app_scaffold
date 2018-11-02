import uuid
from src.db import BaseModel as db
from sqlalchemy.dialects.postgresql import UUID
from src.utils.uuid_converter import str2uuid

class TokenBlacklist(db.Model):
	__tablename__ = 'tokenblacklist'

	tokenblacklistID = db.Column(db.Integer, primary_key=True)
	id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)
	jit = db.Column(db.String())

	
