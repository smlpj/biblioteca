from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)

#! Esta llave no debería estar expuesta públicamente para propósitos comerciales
app.config["SECRET_KEY"] = 'a815622fcd4aac7961bddb66718292de'

# Definición de la URL y configuración de la BD
# TODO: Migrar a PostgreSQL database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///biblioteca.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
from biblioteca import models

# Configuración del módulo ADMIN
admin = Admin(app)
admin.add_view(models.BookView(models.Book, db.session))
admin.add_view(models.AuthorView(models.Author, db.session))

# Importar rutas y modelos
from biblioteca import routes