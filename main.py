from flask import Flask,redirect,url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
TEMPLATES_AUTO_RELOAD=True
app = Flask(__name__)
app.secret_key = "thelastpasswordset"
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Books(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    collection = db.Column(db.String(100))
    coln = db.Column(db.Integer,primary_key=False)

    def __init__(self,name,collection,coln):
        self.name = name
        self.collection = collection
        self.coln = coln

@app.route("/view",methods=['POST','GET'])
def view():
    if request.method == "POST":
        a = 1
        find_book = request.form["search"]
        for i in Books.query.all():
            if i.name == find_book:
                flash(i.name + "  " + i.collection + "  " + str(i.coln))
                a = 0
        if a == 1:
            flash("You don't have that book")
    return render_template("view.html", value=Books.query.all())

@app.route("/",methods=['POST','GET'])
def home():
    a = 1
    if request.method == "POST":
            book = request.form["book"]
            collection = request.form["collection"]
            coln = request.form["coln"]
            for i in Books.query.all():
                if i.name == book:
                    a = 0
                    flash("You already have that book")
            if a == 1:
                nbook = Books(book,collection,coln)
                db.session.add(nbook)
                db.session.commit()
                a = 1
            return redirect("/")
    return render_template("index.html")

@app.route("/erase")
def erase():
        my_row = Books.query.all()
        for i in my_row:
            db.session.delete(i)
            db.session.commit()
        return render_template("erase.html", value=Books.query.all())
    
@app.route("/search",methods=["POST","GET"])
def search():
    if request.method == "POST":
        fbook = request.form["search"]
        for i in Books.query.all():
            if i.name == fbook:
                flash("You already have that book")
                flash(i.name + "   " + i.collection + "   " + str(i.coln))
            else:
                flash("You don't have that book")
    return render_template("search.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)