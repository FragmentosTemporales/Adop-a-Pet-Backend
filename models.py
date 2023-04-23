from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    users = db.relationship("User", back_populates="rol", overlaps="user")
    pets = db.relationship("Pet")
    posts = db.relationship("Post")
    
    def serialize(self):
        return {
            "id" : self.id,  
            "name" : self.name,
            "users" : [user.serialize() for user in self.users],
            "pets" : [pet.serialize() for pet in self.pets],
            "posts" : [post.serialize() for post in self.posts]
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    favorites = db.relationship("Favorites")
    
    rol = db.relationship("Rol", back_populates="users", overlaps="user")
    forms = db.relationship("Form", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "rol_id": self.rol_id
        }
      
class User_description(db.Model):
    __tablename__ = 'description'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    motivation = db.Column(db.String(500), nullable=False)
    style = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "motivation" : self.motivation,
            "style" : self.style,
            "user_id" :  self.user_id
        }
           
class Pet(db.Model):
    __tablename__ = 'pet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    img = db.Column(db.String(100), default = '')
    medical_history = db.Column(db.String(500), nullable=False)
    is_adopted = db.Column(db.Boolean, unique=False, default=False)
    adress_id = db.Column(db.String(500), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
    
    def serialize(self):
        return {
            "id" : self.id,  
            "name" : self.name, 
            "gender" : self.gender, 
            "age"  : self.age,
            "description" : self.description,
            "species" : self.species,
            "size" : self.size,
            'img': self.img,
            "medical_history" : self.medical_history,
            "is_adopted" : self.is_adopted,
            "adress_id" :  self.adress_id,
            "rol_id" : self.rol_id
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def serialize(self):
        return {
            "id": self.id,
            "pet_id" : self.pet_id,
            "user_id" : self.user_id
        }
        
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    #imagePost = db.Column(db.LargeBinary, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))

    def serialize(self):
        return {
            "id" : self.id,  
            "title" : self.title,
            "date" : self.date,
            "description": self.description,
           # "imagePost" : self.imagePost
            "rol_id": self.rol_id
            
        }
    
class Adress(db.Model):
    __tablename__ = 'adress'
    id = db.Column(db.Integer, primary_key=True)
    commune = db.Column(db.String(50), nullable=False)
    pet_id = db.Column(db.Integer,  nullable=False)

    def serialize(self):
        return {
            "id" : self.id,  
            "commune" : self.commune,
            "pet_id": self.pet_id
            
        }
        
class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    query1 = db.Column(db.String(500), nullable=False)
    query2 = db.Column(db.String(500), nullable=False)
    query3 = db.Column(db.String(500), nullable=False)
    query4 = db.Column(db.String(500), nullable=False)
    query5 = db.Column(db.String(500), nullable=False)
    query6 = db.Column(db.String(500), nullable=False)
    query7 = db.Column(db.String(500), nullable=False)
    query8 = db.Column(db.String(500), nullable=False)
    query9 = db.Column(db.String(500), nullable=False)
    query10 = db.Column(db.String(500), nullable=False)
    query11 = db.Column(db.String(500), nullable=False)
    query12 = db.Column(db.String(500), nullable=False)
    query13 = db.Column(db.String(500), nullable=False)
    query14 = db.Column(db.String(500), nullable=False)
    query15 = db.Column(db.String(500), nullable=False) 
    query16 = db.Column(db.String(10), nullable=False)
    query17 = db.Column(db.String(500), nullable=False)
    query18 = db.Column(db.String(10), nullable=False)
    query19 = db.Column(db.String(500), nullable=False)
    query20 = db.Column(db.String(10), nullable=False)
    query21 = db.Column(db.String(10), nullable=False)
    query22 = db.Column(db.String(10), nullable=False)
    query23 = db.Column(db.String(500), nullable=False)
    query24 = db.Column(db.String(500), nullable=False)
    query25 = db.Column(db.String(500), nullable=False)
    query26 = db.Column(db.String(10), nullable=False)
    query27 = db.Column(db.String(10), nullable=False)
    query28 = db.Column(db.String(500), nullable=False)
    query29 = db.Column(db.String(500), nullable=False)
    query30 = db.Column(db.String(10), nullable=False)
    query31 = db.Column(db.String(500), nullable=False)
    query32 = db.Column(db.String(500), nullable=False)
    query33 = db.Column(db.String(500), nullable=False)
    query34 = db.Column(db.String(500), nullable=False)
    query35 = db.Column(db.String(500), nullable=False)
    query36 = db.Column(db.String(10), nullable=False)
    query37 = db.Column(db.String(10), nullable=False)
    query38 = db.Column(db.String(10), nullable=False)
    query39 = db.Column(db.String(500), nullable=False)
    query40 = db.Column(db.String(500), nullable=False)
    query41 = db.Column(db.String(500), nullable=False)
    query42 = db.Column(db.String(500), nullable=False)
    query43 = db.Column(db.String(10), nullable=False)
    query44 = db.Column(db.String(10), nullable=False)
    
    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,            
            "query1" : self.query1,
            "query2" : self.query2,
            "query3" : self.query3,
            "query4" : self.query4,
            "query5" : self.query5,
            "query6" : self.query6,
            "query7" : self.query7,
            "query8" : self.query8,
            "query9" : self.query9,
            "query10" : self.query10,
            "query11" : self.query11,
            "query12" : self.query12,
            "query13" : self.query13,
            "query14" : self.query14,
            "query15" : self.query15,
            "query16" : self.query16,
            "query17" : self.query17,
            "query18" : self.query18,
            "query19" : self.query19,
            "query20" : self.query20,
            "query21" : self.query21,
            "query22" : self.query22,
            "query23" : self.query23,
            "query24" : self.query24,
            "query25" : self.query25,
            "query26" : self.query26,
            "query27" : self.query27,
            "query28" : self.query28,
            "query29" : self.query29,
            "query30" : self.query30,
            "query31" : self.query31,
            "query32" : self.query32,
            "query33" : self.query33,
            "query34" : self.query34,
            "query35" : self.query35,
            "query36" : self.query36,
            "query37" : self.query37,
            "query38" : self.query38,
            "query39" : self.query39,
            "query40" : self.query40,
            "query41" : self.query41,
            "query42" : self.query42,
            "query43" : self.query43,
            "query44" : self.query44,
            "user": self.user.name + " " + self.user.last_name
    
            
        }