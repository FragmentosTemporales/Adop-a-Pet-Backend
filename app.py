import os

from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
from models import db , Rol, User, User_description, Pet, Favorites, Post, Adress, Form
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors  import CORS
from datetime import datetime
from flask_cors import CORS


upload_folder = os.path.join('static', 'uploads')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = "super-secreta"
app.config['UPLOAD'] = upload_folder
db.init_app(app)   

migrate = Migrate(app, db)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

@app.route("/")
def home():
    return "Hello world"

# ROL

# POST

@app.route("/rols", methods=["POST"])
def create_rol():
    rol = Rol()
    rol.name = request.json.get("name")

    db.session.add(rol)
    db.session.commit()

    return "Usuario guardado", 201

# GET

@app.route("/rols/list", methods=["GET"])
def get_rols():
    rols = Rol.query.all()
    result = []
    for rol in rols:
        result.append(rol.serialize())
    return jsonify(result)

# PUT & DELETE


@app.route("/rols/<int:id>", methods=["PUT", "DELETE"])
def update_rol(id):
    rol = Rol.query.get(id)
    if rol is not None:
        if request.method == "DELETE":
            db.session.delete(rol)
            db.session.commit()
            return jsonify("Usuario eliminado"), 204
        else:
            rol.name = request.json.get("name")
            db.session.commit()
            return jsonify("Usuario actualizado"), 200
    return jsonify("Usuario no encontrado"), 404


# USER

# POST

@app.route("/users", methods=["POST"])
def create_user():
    # Obtiene los datos del usuario de la solicitud
    name = request.json.get("name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    phone = request.json.get("phone")
    rol_id = request.json.get("rol_id")
    password = request.json.get("password")
    password_hash = generate_password_hash(password)
    password = password_hash

    # Verifica si el correo ya existe en la base de datos
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify("El correo ya existe en la base de datos"), 400

    # Crea un nuevo objeto User
    new_user = User(name=name, last_name=last_name, email=email,
                    phone=phone, rol_id=rol_id, password=password)

    # Agrega el usuario a la sesión de la base de datos
    db.session.add(new_user)
    db.session.commit()

    # Devuelve una respuesta con código de estado HTTP 201
    return jsonify("Usuario guardado"), 201

# LOGIN


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    user = User.query.filter_by(email=email).first()
    if user is not None:
        is_valid = check_password_hash(user.password, password)
        if is_valid:
            access_token = create_access_token(identity=email)
            return jsonify({
                "token": access_token,
                "user_id": user.id,
                "rol_id": user.rol_id,
                "email": user.email,

            }), 200
        else:
            return jsonify("La contraseña es incorrecta"), 400
    else:
        return jsonify("El usuario no existe o la información es inválida"), 400


# GET

@app.route("/users/list", methods=["GET"])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result)

# GET USER BY ID


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        return jsonify(user.serialize())
    else:
        return jsonify("Usuario no encontrado"), 404


# PUT & DELETE

@app.route("/users/<int:id>", methods=["PUT", "DELETE"])
def update_user(id):    
    user = User.query.get(id)    
    if user is not None:
        if request.method == "DELETE":
            user_description = User_description.query.filter_by(user_id=id).first()
            if user_description is not None:
                db.session.delete(user_description)
            form = Form.query.filter_by(user_id=id).first()
            if form is not None:
                db.session.delete(form)
            favorites = Favorites.query.filter_by(user_id=id).all()
            for favorite in favorites:
                db.session.delete(favorite)
            db.session.delete(user)
            db.session.commit()
            return jsonify("Usuario, descripción, formulario y favoritas eliminados"), 204

        else:
            user.name = request.json.get("name")
            user.last_name = request.json.get("last_name")
            user.phone = request.json.get("phone")
            user.email = request.json.get("email", user.email)
            user.rol_id = request.json.get("rol_id", user.rol_id)
            user.password = request.json.get("password", user.password)

            db.session.commit()
            return jsonify("Usuario actualizado"), 200
    return jsonify("Usuario no encontrado"), 404



# USER_DESCRIPTION

# POST

@app.route("/users/description/", methods=["POST"])
@jwt_required()
def create_description():
    user_description = User_description()
    user_description.description = request.json.get("description")
    user_description.motivation = request.json.get("motivation")
    user_description.style = request.json.get("style")
    user_description.user_id = request.json.get("user_id")

    existing_description = User_description.query.filter_by(
        user_id=request.json.get("user_id")).first()
    if existing_description:
        db.session.delete(existing_description)
        db.session.commit()

    db.session.add(user_description)
    db.session.commit()

    return jsonify("Descripción guardada"), 201

# GET


@app.route("/descriptions/list", methods=["GET"])
def get_description():
    user_descriptions = User_description.query.all()
    result = []
    for user_description in user_descriptions:
        result.append(user_description.serialize())
    return jsonify(result)

# GET user with description


@app.route("/users/description/<int:id>", methods=["GET"])
@jwt_required()
def get_user_with_description(id):
    user = User.query.filter_by(id=id).first()  # Obtener el usuario por su id
    if user is not None:
        user_description = User_description.query.filter_by(
            user_id=id).first()  # Obtener la descripción del usuario por su id
        if user_description is not None:
            # Crear un diccionario con los datos del usuario y su descripción
            result = {
                "user_id": user.id,
                "name": user.name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "rol_id": user.rol_id,
                "description": user_description.description,
                "motivation": user_description.motivation,
                "style": user_description.style
            }
            return jsonify(result), 200
        else:
            return jsonify("Descripción del usuario no encontrada"), 404
    else:
        return jsonify("Usuario no encontrado"), 404

# PUT & DELETE


@app.route("/description/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_description(id):
    user_description = User_description.query.get(id)
    if user_description is not None:
        if request.method == "DELETE":
            db.session.delete(user_description)
            db.session.commit()
            return jsonify("Description eliminada"), 204
        else:
            user_description.description = request.json(
                "description", user_description.description)
            user_description.motivation = request.json(
                "motivation", user_description.motivation)
            user_description.style = request.json(
                "style", user_description.style)
            user_description.user_id = request.json(
                "user_id", user_description.user_id)

            db.session.commit()

            return jsonify("Descripción actualizada"), 200

    return jsonify("Descripción no encontrada"), 404


# PET

# POST

@app.route("/pets", methods=["POST"])
def create_pet():
    print(request.form)
    print(request.files)
    pet = Pet()
    pet.name = request.form["name"]
    pet.gender = request.form["gender"]
    pet.age = request.form["age"]
    pet.description = request.form["description"]
    pet.species = request.form["species"]
    pet.size = request.form["size"]
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD'], filename))
    pet.img = filename
    pet.medical_history = request.form["medical_history"]
    pet.is_adopted = bool(request.form["is_adopted"])
    pet.adress_id = request.form["adress_id"]
    pet.rol_id = request.form["rol_id"]
   
    db.session.add(pet)
    db.session.commit()

    print(pet)
    return jsonify("Mascota guardada"), 201


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD"], name)


@app.route('/pets/search' , methods=['POST'])
def search_pets():
    gender = request.json.get("gender")
    size = request.json.get("size")
    species = request.json.get("species")

    pets_query = Pet.query
    if gender:
        pets_query = pets_query.filter_by(gender=gender)
    if size:
        pets_query = pets_query.filter_by(size=size)
    if species:
        pets_query = pets_query.filter_by(species=species)

    pets = pets_query.all()
    pets = list(map(lambda pet: pet.serialize(), pets))

    return jsonify(pets), 200


@app.route('/pet/<int:id>', methods=['GET'])
def get_planet_id(id):
    pet = Pet.query.get(id)
    if pet is not None:
        return jsonify(pet.serialize())
    else:
        return jsonify('No se encontró el objeto People con el ID especificado')


# GET

@app.route("/pets/list", methods=["GET"])
def get_pets():
    pets = Pet.query.all()
    result = []
    for pet in pets:
        result.append(pet.serialize())
    return jsonify(result)

# PUT & DELETE

@app.route("/pet/<int:id>", methods=["PUT", "DELETE"])
def update_pet(id):
    pet = Pet.query.get(id)
    if pet is not None:
        if request.method == "DELETE":
            db.session.delete(pet)
            db.session.commit()
            return jsonify("Mascota eliminada"), 204
        else:
            print(request.files)
            if 'name' in request.form:
                pet.name = request.form["name"]
            if 'gender' in request.form:
                pet.gender = request.form["gender"]
            if 'age' in request.form:
                pet.age = request.form["age"]
            if 'description' in request.form:
                pet.description = request.form["description"]
            if 'species' in request.form:
                pet.species = request.form["species"]
            if 'size' in request.form:
                pet.size = request.form["size"]
            if 'file' in request.files:
                file = request.files['file']
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD'], filename))
                pet.img = filename
            if 'medical_history' in request.form:
                pet.medical_history = request.form["medical_history"]
            if 'is_adopted' in request.form:
                pet.is_adopted = bool(request.form["is_adopted"])
            if 'adress_id' in request.form:
                pet.adress_id = request.form["adress_id"]
            if 'rol_id' in request.form:
                pet.rol_id = request.form["rol_id"]
            
            print(request.form)
            
            db.session.commit()
        
            return jsonify("Mascota actualizada"), 200
    
    return jsonify("Mascota no encontrada"), 404 


# FAVORITES

# POST

@app.route("/favorites", methods=["POST"])
@jwt_required()
def create_favorite():
    pet_id = request.json.get("pet_id")
    user_id = request.json.get("user_id")
    
    # Check if the user already has a pet with the same id registered
    existing_favorite = Favorites.query.filter_by(pet_id=pet_id, user_id=user_id).first()
    if existing_favorite:
        return jsonify("El usuario ya tiene una mascota con el mismo id registrada"), 400
    
    # If the user does not have a pet with the same id registered, create a new favorite
    favorites = Favorites()
    favorites.pet_id = pet_id
    favorites.user_id = user_id
    db.session.add(favorites)
    db.session.commit()
    
    return jsonify("Favorito guardado"), 201

# GET


@app.route("/favorites/list", methods=["GET"])
def get_favorites():
    favorites = Favorites.query.all()
    result = []
    for favorite in favorites:
        result.append(favorite.serialize())
    return jsonify(result)

# GET favorite/user


@app.route("/favorites/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_favorite_user(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    pet_list = []
    for favorite in favorites:
        pet = Pet.query.get(favorite.pet_id)
        if pet is not None:
            pet_list.append(pet.serialize())
    return jsonify(pet_list)

@app.route("/favorites/<int:user_id>/<int:pet_id>", methods=["PUT", "DELETE"])
def update_favorites(user_id, pet_id):
    favorite = Favorites.query.filter_by(user_id=user_id, pet_id=pet_id).first()
    if favorite is not None:
        if request.method == "DELETE":
            db.session.delete(favorite)
            db.session.commit()
            return jsonify("Favorito eliminado"), 204
        else:
            favorite.pet_id = request.json.get("pet_id")
            favorite.user_id = request.json.get("user_id")
            db.session.commit()
            return jsonify("Favoritos actualizados"), 200
    return jsonify("Favoritos no encontrados"), 404


# POST

# POST

@app.route("/posts", methods=["POST"])
def create_post():
    posts = Post()
    posts.title = request.json.get("title")
    posts.date = datetime.strptime(request.json.get("date") +" 00:00:00","%Y-%m-%d %H:%M:%S")
    posts.description = request.json.get("description")
    #posts.imagepost = request.json.get("image")
    posts.rol_id = request.json.get("rol_id")

    db.session.add(posts)
    db.session.commit()

    return jsonify("Publicación guardada"), 201
    
#GET    

# GET


@app.route("/posts/list", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    result = []
    for post in posts:
        result.append(post.serialize())
    return jsonify(result)

# PUT & DELETE


@app.route("/posts/<int:id>", methods=["PUT", "DELETE"])
def update_posts(id):
    post = Post.query.get(id)
    if post is not None:
        if request.method == "DELETE":
            db.session.delete(post)
            db.session.commit()

            return jsonify("Publicación eliminada"), 204
        else:
            title = request.json.get("title")
            if title is not None:
                post.title = title
            description = request.json.get("description")
            if description is not None:
                post.description = description
            rol_id = request.json.get("rol_id")
            if rol_id is not None:
                post.rol_id = rol_id

            db.session.commit()

            return jsonify("Publicación actualizada!"), 200

    return jsonify("Publicación no encontrada"), 404


# ADRESS

# POST

@app.route("/adress", methods=["POST"])
def create_adress():
    adress = Adress()
    adress.commune = request.json.get("commune")
    adress.pet_id = request.json.get("pet_id")
    adress.pet_id = request.json.get("pet_id")

    
    adress.pet_id = request.json.get("pet_id")    

    
    db.session.add(adress)
    db.session.commit()

    return jsonify("Dirección guardada"), 201

# GET


@app.route("/adress/list", methods=["GET"])
def get_adress():
    adress = Adress.query.all()
    result = []
    for adress in adress:
        result.append(adress.serialize())
    return jsonify(result)

# PUT & DELETE


@app.route("/adress/<int:id>", methods=["PUT", "DELETE"])
def update_adress(id):
    adress = Adress.query.get(id)
    if adress is not None:
        if request.method == "DELETE":
            db.session.delete(adress)
            db.session.commit()

            return jsonify("Ubicación eliminada"), 204
        else:
            commune = request.json.get("commune")
            pet_id = request.json.get("pet_id")
            if commune is not None:
                adress.commune = commune
            if pet_id is not None:
                adress.pet_id = pet_id

            db.session.commit()

            return jsonify("Ubicación actualizada"), 200

    return jsonify("Ubicación no encontrada"), 404


# FORM

# POST

@app.route("/form", methods=["POST"])
@jwt_required()
def create_form():
    form = Form()
    form.user_id = request.json.get("user_id")
    form.query1 = request.json.get("query1")
    form.query2 = request.json.get("query2")
    form.query3 = request.json.get("query3")
    form.query4 = request.json.get("query4")
    form.query5 = request.json.get("query5")
    form.query6 = request.json.get("query6")
    form.query7 = request.json.get("query7")
    form.query8 = request.json.get("query8")
    form.query9 = request.json.get("query9")
    form.query10 = request.json.get("query10")
    form.query11 = request.json.get("query11")
    form.query12 = request.json.get("query12")
    form.query13 = request.json.get("query13")
    form.query14 = request.json.get("query14")
    form.query15 = request.json.get("query15")
    form.query16 = request.json.get("query16")
    form.query17 = request.json.get("query17")
    form.query18 = request.json.get("query18")
    form.query19 = request.json.get("query19")
    form.query20 = request.json.get("query20")
    form.query21 = request.json.get("query21")
    form.query22 = request.json.get("query22")
    form.query23 = request.json.get("query23")
    form.query24 = request.json.get("query24")
    form.query25 = request.json.get("query25")
    form.query26 = request.json.get("query26")
    form.query27 = request.json.get("query27")
    form.query28 = request.json.get("query28")
    form.query29 = request.json.get("query29")
    form.query30 = request.json.get("query30")
    form.query31 = request.json.get("query31")
    form.query32 = request.json.get("query32")
    form.query33 = request.json.get("query33")
    form.query34 = request.json.get("query34")
    form.query35 = request.json.get("query35")
    form.query36 = request.json.get("query36")
    form.query37 = request.json.get("query37")
    form.query38 = request.json.get("query38")
    form.query39 = request.json.get("query39")
    form.query40 = request.json.get("query40")
    form.query41 = request.json.get("query41")
    form.query42 = request.json.get("query42")
    form.query43 = request.json.get("query43")
    form.query44 = request.json.get("query44")

    db.session.add(form)
    db.session.commit()

    return jsonify("Formulario guardado"), 201

# GET


@app.route("/form/list", methods=["GET"])
def get_form():
    form = Form.query.all()
    result = []
    for form in form:
        result.append(form.serialize())
    return jsonify(result)


# PUT & DELETE

@app.route("/form/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_form(id):
    form = Form.query.get(id)
    if form is not None:
        if request.method == "DELETE":
            db.session.delete(form)
            db.session.commit()

            return jsonify("Publicación eliminada"), 204
        else:
            form.user_id = request.json.get("user_id")
            form.query1 = request.json.get("query1")
            form.query2 = request.json.get("query2")
            form.query3 = request.json.get("query3")
            form.query4 = request.json.get("query4")
            form.query5 = request.json.get("query5")
            form.query6 = request.json.get("query6")
            form.query7 = request.json.get("query7")
            form.query8 = request.json.get("query8")
            form.query9 = request.json.get("query9")
            form.query10 = request.json.get("query10")
            form.query11 = request.json.get("query11")
            form.query12 = request.json.get("query12")
            form.query13 = request.json.get("query13")
            form.query14 = request.json.get("query14")
            form.query15 = request.json.get("query15")
            form.query16 = request.json.get("query16")
            form.query17 = request.json.get("query17")
            form.query18 = request.json.get("query18")
            form.query19 = request.json.get("query19")
            form.query20 = request.json.get("query20")
            form.query21 = request.json.get("query21")
            form.query22 = request.json.get("query22")
            form.query23 = request.json.get("query23")
            form.query24 = request.json.get("query24")
            form.query25 = request.json.get("query25")
            form.query26 = request.json.get("query26")
            form.query27 = request.json.get("query27")
            form.query28 = request.json.get("query28")
            form.query29 = request.json.get("query29")
            form.query30 = request.json.get("query30")
            form.query31 = request.json.get("query31")
            form.query32 = request.json.get("query32")
            form.query33 = request.json.get("query33")
            form.query34 = request.json.get("query34")
            form.query35 = request.json.get("query35")
            form.query36 = request.json.get("query36")
            form.query37 = request.json.get("query37")
            form.query38 = request.json.get("query38")
            form.query39 = request.json.get("query39")
            form.query40 = request.json.get("query40")
            form.query41 = request.json.get("query41")
            form.query42 = request.json.get("query42")
            form.query43 = request.json.get("query43")
            form.query44 = request.json.get("query44")
            
            
        

        
            db.session.commit()

            return jsonify("Formulario actualizado"), 200

    return jsonify("Formulario no encontrado"), 404


if __name__ == "__main__":
    app.run(host="localhost", port="8080")
