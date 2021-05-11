from biblioteca import app
from biblioteca.models import *
from flask import request, render_template


@app.route('/')
def home():
    return "Hola mundo, soy una biblioteca!"

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
