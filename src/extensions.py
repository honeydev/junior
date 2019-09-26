from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import Model, SQLAlchemy
from flask_session import Session


class CRUDMixin(Model):

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, field_value in kwargs.items():
            setattr(self, attr, field_value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


bcrypt = Bcrypt()
db = SQLAlchemy(model_class=CRUDMixin)
migrate = Migrate()
admin = Admin(name='junnior', template_mode='bootstrap3')
sess = Session()
