from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bakery'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)

def serialize_cupcakes(cupcake):
    """Serializes a desert SQLAlchemy obj to dictionary"""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Returns all the cupcakes as JSON"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcakes(c) for c in cupcakes]

    return (jsonify(cupcakes=serialized), 200)

@app.route("/api/cupcakes/<int:cupcake_id>")
def list_a_cupcake(cupcake_id):
    """Returns a cupcake as JSON"""

    cupcake = Cupcake.query.get(cupcake_id)
    serialized = serialize_cupcakes(cupcake)

    return (jsonify(cupcake=serialized), 200)

@app.route("/api/cupcakes", methods=["POST"])
def new_cupcake():
    """Adds a new cupcake to the database"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcakes(cupcake)
    return ( jsonify(cupcake=serialized), 201 )

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake's information"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    serialized = serialize_cupcakes(cupcake)
    return (jsonify(cupcake=serialized), 200)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a cupcake from the database"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return (jsonify(message="deleted"), 200)

@app.route("/")
def display_index():
    """Shows off the index page"""
    return render_template("index.html")