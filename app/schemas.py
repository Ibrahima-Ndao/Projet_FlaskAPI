from app import ma
from app.models import User, ElectronicProduct

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)

class ElectronicProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ElectronicProduct
        load_instance = True
