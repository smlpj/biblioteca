from datetime import date

from flask import Markup
from sqlalchemy import func
from flask_admin.contrib.sqla import ModelView

from biblioteca import db


class Book(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", back_populates="books_written")
    amount_total = db.Column(db.Integer, nullable=False)
    amount_available = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(15), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    rating = db.Column(db.Float(), nullable=False)
    local_picture_route = db.Column(db.String(128))
    online_picture_route = db.Column(db.String(255))
    format = db.Column(db.String(50), nullable=False)
    loans = db.relationship("Loan", back_populates="loaned_book")
    
    def __repr__(self):
        return f"<Book: {self.title} by {self.author.name}>"
    

class Author(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    books_written = db.relationship("Book", back_populates="author")
    
    def __repr__(self):
        return f"<Author: {self.name}>"
    
    @property
    def amount_books_written(self):
        return len(self.books_written)
        
class Loan(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    loaner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    loaner = db.relationship("User", back_populates="loans")
    loaned_book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    loaned_book = db.relationship("Book", back_populates="loans")
    takeout_date = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean(), default=False)
    return_date = db.Column(db.Date)
    

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    num_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.Integer)
    password = db.Column(db.String(255), nullable=False)
    loans = db.relationship("Loan", back_populates="loaner")
    
    @property
    def current_loans(self):
        curr_loans = [loan for loan in self.loans if loan.returned]
    
    
class BookView(ModelView):
    column_exclude_list = ["online_picture_route", "local_picture_route"]
    column_searchable_list = ['title', 'isbn']
    column_filters = ['author']
    page_size = 30


class AuthorView(ModelView):
    
    column_list = ("name", "amount_books_written")
    
    