from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    memberships = db.relationship('Membership', backref="contact")

    @classmethod
    def create(cls, **kwargs):
        """Create and return a new instance"""
        return cls(**kwargs)
    
    @classmethod
    def contact_all(cls):
        """ Return all contacts as a json """
        return cls.query.all()

    @classmethod
    def get_contact_by_id(cls, id):
        """Get a contact for your id"""
        return cls.query.get(id)
    
    @classmethod
    def delete_contact_by_id(cls,id):
        """"Delete a contact by id"""
        db.session.delete(id) 
        db.session.commit();

    def save(self):
        """Save and commit a new contact"""
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "memberships": [m.group.serialize() for m in self.memberships],
        }



class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    memberships = db.relationship('Membership', backref="group")

    @classmethod
    def get_all_groups(cls):
        return cls.query.all();

    @classmethod
    def create(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def get_group_by_id(cls, id):
        """Get a contact for your id"""
        return cls.query.get(id)

    @classmethod
    def delete_group_by_id(cls,id):
        """"Delete a contact by id"""
        db.session.delete(id) 
        db.session.commit();
    
    def save(self):
        """Save and commit a new contact"""
        db.session.add(self)
        db.session.commit()  

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "memberships": [m.contact.serialize() for m in self.memberships],
        }



class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

