from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


app.config['SECRET_KEY'] = 'topsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/catalog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


db = SQLAlchemy(app)


@app.route("/index")
@app.route("/")
def hello_world():
    return "Hello Flask"


@app.route("/new/")
def query_string(greeting="holla"):
    query_val = request.args.get("greeting", greeting)
    return "<h1> the greeting is {}".format(query_val)


@app.route("/user")
@app.route("/user/<name>")
def no_query_strings(name="mina"):
    return "<h1>hello there! {}</h1>".format(name)


@app.route("/text/<string:name>")
def working_with_strings(name):
    return "there is a string {}".format(name)


@app.route("/number/<int:number>")
def working_with_numbers(number):
    return "there is a number: {}".format(number)


@app.route("/temp")
def using_templates():
    return render_template("hello.html")

@app.route("/watch")
def movies_2017():
    movie_list = ["autopsy of jane doe",
                  "neon demon",
                  "ghost in a shell",
                  "kong: skull island",
                  "john wick 2",
                  "spiderman - homecoming"]
    return render_template("movies.html",
                            movies=movie_list,
                            name="Herry")


@app.route("/tables")
def movie_plus():
    movie_dict = {"autopsy of jane doe": 2.14,
                  "neon demon": 3.20,
                  "ghost in a shell": 1.50,
                  "kong: skull island": 3.50,
                  "john wick 2": 02.52,
                  "spiderman - homecoming": 1.48}
    return render_template("table_data.html",
                            movies=movie_dict,
                            name="Sally")


@app.route("/filters")
def filter_data():
    movies_dict = {"autopsy of jane doe": 2.14,
                  "neon demon": 3.20,
                  "ghost in a shell": 1.50,
                  "kong: skull island": 3.50,
                  "john wick 2": 02.52,
                  "spiderman - homecoming": 1.48}
    return render_template("filter_data.html",
                            movies=movies_dict,
                            name=None,
                            film="a christmas carol")


@app.route("/macros")
def jinja_macros():
    movies_dict = {"autopsy of jane doe": 2.14,
                  "neon demon": 3.20,
                  "ghost in a shell": 1.50,
                  "kong: skull island": 3.50,
                  "john wick 2": 02.52,
                  "spiderman - homecoming": 1.48}
    return render_template("using_macros.html", movies=movies_dict)


class Publication(db.Model):
    __tablename__ = "publication"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Publisher is {}".format(self.name)


if __name__ == "__main__":
    app.run(debug=1)
    db.create_all()

class Book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey("publication.id"))

    def __init__(self, title, author, avg_rating, format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)