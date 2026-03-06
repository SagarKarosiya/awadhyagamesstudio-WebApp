from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

# -------------------
# FOLDERS
# -------------------

os.makedirs("static/uploads/covers", exist_ok=True)
os.makedirs("static/uploads/screenshots", exist_ok=True)

UPLOAD_FOLDER = "static/uploads"

# -------------------
# FLASK APP
# -------------------

app = Flask(__name__)
app.secret_key = "secret123"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------
# DATABASE MODELS
# -------------------

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)


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

    return render_template(
        "index.html",
        featured_game=featured_game,
        games=games,
        posts=posts
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/games")
def games():

    games = Game.query.all()

    return render_template("games.html", games=games)


@app.route("/game/<int:id>")
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

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        new_message = Contact(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_message)
        db.session.commit()

    return render_template("contact.html")


@app.route("/subscribe", methods=["POST"])
def subscribe():

    email = request.form["email"]

    sub = Subscriber(email=email)

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

    games_count = Game.query.count()
    posts_count = Blog.query.count()
    subs_count = Subscriber.query.count()
    messages_count = Contact.query.count()

    return render_template(
        "admin/dashboard.html",
        games=games,
        posts=posts,
        games_count=games_count,
        posts_count=posts_count,
        subs_count=subs_count,
        messages_count=messages_count
    )


# -------------------
# ADD GAME
# -------------------

@app.route("/add_game", methods=["GET", "POST"])
def add_game():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        trailer = request.form["trailer"]
        featured = request.form.get("featured")

        cover_file = request.files.get("cover")

        cover_path = ""

        if cover_file and cover_file.filename != "":

            filename = secure_filename(cover_file.filename)

            cover_path = os.path.join("static/uploads/covers", filename)

            cover_file.save(cover_path)

        new_game = Game(
            title=title,
            description=description,
            trailer=trailer,
            cover=cover_path,
            featured=True if featured else False
        )

        db.session.add(new_game)
        db.session.commit()

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

    file = request.files.get("image")

    if not file or file.filename == "":
        return redirect(url_for("game_detail", id=game_id))

    filename = secure_filename(file.filename)

    path = os.path.join("static/uploads/screenshots", filename)

    file.save(path)

    shot = Screenshot(
        game_id=game_id,
        image=path
    )

    db.session.add(shot)
    db.session.commit()

    return redirect(url_for("game_detail", id=game_id))


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

@app.route("/add_post", methods=["GET", "POST"])
def add_post():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        post = Blog(title=title, content=content)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("admin/add_post.html")


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

    app.run(debug=True)