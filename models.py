from peewee import Model, CharField, MySQLDatabase
from config import Config

db = MySQLDatabase(Config.MYSQL_DB, user=Config.MYSQL_USER, password=Config.MYSQL_PASSWORD, host=Config.MYSQL_HOST)

class Book(Model):
    title = CharField()
    description = CharField()
    author = CharField()

    class Meta:
        database = db
        db_table = 'books'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'author': self.author
        }