from biblioteca import app
from biblioteca.models import *
from flask import request, render_template, redirect, url_for


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/books")
def books():
    page = request.args.get('page', 1, type=int)
    books = Book.query.paginate(page=page, per_page=5)
    return render_template("books.html", books=books)

@app.route("/author/<author_name>")
def author_page(author_name):
    author = Author.query.filter(Author.name == author_name).first()
    if author:
        page = request.args.get('page', 1, type=int)
        books = Book.query.filter(Book.author == author).paginate(page=page, per_page=5)
        return render_template("author.html", author=author, books=books)
    
@app.route("/search", methods=["POST"])
def search():
    if "simple_search" in request.form:
        if request.form["simple_search"] == "":
            return redirect(url_for('home'))
        else:
            return redirect(url_for('results', name=request.form["simple_search"]))
        

@app.route("/results")
def results():
    page = request.args.get('page', 1, type=int)
    
    books = db.session.query(Book)
    if "name" in request.args:
        print("Búsqueda por nombre")
    
    books = books.paginate(page=page, per_page=12)
    return render_template("results.html", books=books)

@app.route("/login")
def login():
    pass