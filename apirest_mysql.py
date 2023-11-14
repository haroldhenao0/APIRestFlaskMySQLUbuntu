from flask import Flask, jsonify, request, abort
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView
from models import db, Book
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Conectar a la base de datos antes de la primera solicitud
@app.before_first_request
def initialize_database():
    db.connect()

# Cerrar la conexión de la base de datos después de cada solicitud
@app.teardown_appcontext
def close_database(exception=None):
    if not db.is_closed():
        db.close()

# Flask-Admin
admin = Admin(app, name='MyBookApp', template_mode='bootstrap4')
admin.add_view(ModelView(Book))

# Endpoint para listar todos los libros
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.select()
    return jsonify({'books': [book.to_dict() for book in books]})

# Endpoint para obtener un libro por ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.get_or_none(Book.id == book_id)
    if book:
        return jsonify({'book': book.to_dict()})
    abort(404)

# Endpoint para crear un nuevo libro
@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = Book.create(**request.json)
    return jsonify({'book': book.to_dict()}), 201
# Endpoint para actualizar un libro
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.get_or_none(Book.id == book_id)
    if book:
        for key, value in request.json.items():
            setattr(book, key, value)
        book.save()
        return jsonify({'book': book.to_dict()})
    abort(404)

# Endpoint para eliminar un libro
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.get_or_none(Book.id == book_id)
    if book:
        book.delete_instance()
        return jsonify({'result': True})
    abort(404)

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)