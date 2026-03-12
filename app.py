from flask import Flask, render_template, request, redirect, session, url_for , flash
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import sqlite3
from werkzeug.utils import secure_filename

# -------------------
# FOLDERS
# -------------------
os.makedirs("static/uploads/covers", exist_ok=True)
os.makedirs("static/uploads/screenshots", exist_ok=True)

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


# Check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -------------------
# FLASK APP
# -------------------
app = Flask(__name__)
app.secret_key = "secret123"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
database_url = os.environ.get("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------
# DATABASE MODELS
# -------------------

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    trailer = db.Column(db.String(200))
    cover = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    trailer = db.Column(db.String(200))
    cover = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    
    screenshots = db.relationship("Screenshot", backref="game", lazy=True)


class Screenshot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    image = db.Column(db.String(200))


# -------------------
# PUBLIC ROUTES
# -------------------

@app.route("/")
def home():
    featured_game = Game.query.filter_by(featured=True).first()
    games = Game.query.order_by(Game.id.desc()).limit(4)
    posts = Blog.query.order_by(Blog.id.desc()).limit(3)
    return render_template("index.html", featured_game=featured_game, games=games, posts=posts)
# -------------------
# Admin Create
# -------------------
@app.route("/create-admin")
def create_admin():

    admin = User(
        username="admin",
        password="admin123"
    )

    db.session.add(admin)
    db.session.commit()

    return "Admin created"
# -------------------
# Database migration temperary
# -------------------
@app.route("/init-db")
def init_db():
    db.create_all()
    return "Database created"

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/games")
def games_page():
    games = Game.query.all()
    return render_template("games.html", games=games)


@app.route("/games/<int:id>")
def game_detail(id):
    game = Game.query.get_or_404(id)
    return render_template("game_detail.html", game=game)


@app.route("/blog")
def blog():
    posts = Blog.query.order_by(Blog.id.desc()).all()
    return render_template("blog.html", posts=posts)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        new_message = Contact(
            name=request.form["name"],
            email=request.form["email"],
            message=request.form["message"]
        )
        db.session.add(new_message)
        db.session.commit()
    return render_template("contact.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():
    sub = Subscriber(email=request.form["email"])
    db.session.add(sub)
    db.session.commit()
    return redirect("/")


# -------------------
# ADMIN LOGIN
# -------------------

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("dashboard"))
    return render_template("admin/login.html")


# -------------------
# ADMIN DASHBOARD
# -------------------

@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    games = Game.query.all()
    posts = Blog.query.all()
    return render_template(
        "admin/dashboard.html",
        games=games,
        posts=posts,
        games_count=Game.query.count(),
        posts_count=Blog.query.count(),
        subs_count=Subscriber.query.count(),
        messages_count=Contact.query.count()
    )


# -------------------
# ADD GAME
# -------------------

@app.route("/add_game", methods=["GET", "POST"])
def add_game():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form.get("title")
        description = request.form.get("description")
        trailer = request.form.get("trailer")
        featured = True if request.form.get("featured") else False

        cover = request.files.get("cover")
        filename = ""

        if cover and allowed_file(cover.filename):

            ext = cover.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"

            filepath = os.path.join("static/uploads/covers", filename)
            cover.save(filepath)

        new_game = Game(
            title=title,
            description=description,
            trailer=trailer,
            cover=filename,
            featured=featured
        )

        db.session.add(new_game)
        db.session.commit()

        flash("Game added successfully!")
        return redirect(url_for("dashboard"))

    return render_template("admin/add_game.html")

# -------------------
# EDIT GAME
# -------------------

@app.route("/edit_game/<int:id>", methods=["GET", "POST"])
def edit_game(id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    game = Game.query.get_or_404(id)
    if request.method == "POST":
        game.title = request.form["title"]
        game.description = request.form["description"]
        game.trailer = request.form["trailer"]
        game.featured = True if request.form.get("featured") == "1" else False
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("admin/edit_game.html", game=game)


# -------------------
# DELETE GAME
# -------------------

@app.route("/delete_game/<int:id>")
def delete_game(id):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for("dashboard"))


# -------------------
# ADD SCREENSHOT
# -------------------

@app.route("/add_screenshot/<int:game_id>", methods=["POST"])
def add_screenshot(game_id):

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    file = request.files.get("image")

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

        path = os.path.join("static/uploads/screenshots", filename)

        file.save(path)

        shot = Screenshot(
            game_id=game_id,
            image=filename
        )

        db.session.add(shot)
        db.session.commit()

    return redirect(url_for("edit_game", id=game_id))

# -------------------
# VIEW MESSAGES
# -------------------

@app.route("/messages")
def messages():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    msgs = Contact.query.order_by(Contact.id.desc()).all()
    return render_template("admin/messages.html", msgs=msgs)


# -------------------
# ADD BLOG POST
# -------------------

@app.route("/add_post", methods=["GET","POST"])
def add_post():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        trailer = request.form["trailer"]
        featured = True if request.form.get("featured") else False

        cover = request.files.get("cover")
        filename = ""

        if cover and allowed_file(cover.filename):
            filename = secure_filename(cover.filename)
            cover.save(os.path.join("static/uploads", filename))

        post = Blog(
            title=title,
            description=description,
            trailer=trailer,
            cover=filename,
            featured=featured
        )

        db.session.add(post)
        db.session.commit()

        return redirect("/dashboard")

    return render_template("admin/add_post.html")
# -------------------
# Delete Screenshots
# -------------------
@app.route("/delete_screenshot/<int:id>")
def delete_screenshot(id):

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    shot = Screenshot.query.get_or_404(id)

    game_id = shot.game_id

    db.session.delete(shot)
    db.session.commit()

    return redirect(url_for("edit_game", id=game_id))


# -------------------
# LOGOUT
# -------------------

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))


# -------------------
# RUN SERVER
# -------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=10000)