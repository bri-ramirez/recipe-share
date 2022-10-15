from flask import flash
from flask_app.models.models import Model
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User(Model):
    tabla = "users"

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = f"INSERT INTO {cls.tabla} ( first_name , last_name , email, password ) VALUES ( %(fname)s , %(lname)s , %(email)s, %(password)s );" 
        return connectToMySQL(cls.esquema).query_db( query, data )

    @classmethod
    def getByEmail(cls, email):
        query = f"SELECT * FROM {cls.tabla} WHERE email= %(email)s"
        results = connectToMySQL(cls.esquema).query_db(query, {
            "table": cls.tabla,
            "email": email
        })

        if len(results) == 0:
            return False

        return cls(results[0])

    @staticmethod
    def validUser(dataUser):
        is_valid = True

        if len(dataUser['first_name']) < 2:
            flash("El nombre debe poseer al menos 2 caracteres")
            is_valid = False
        if len(dataUser['last_name']) < 2:
            flash("El Apellido debe poseer al menos 2 caracteres")
            is_valid = False
        if not EMAIL_REGEX.match(dataUser['email']): 
            flash("Debe ingresar una dirección de correo válida")
            is_valid = False 
        if not dataUser['password'] == dataUser['password_confirm']:
            flash("Las contraseñan no coinciden")
            is_valid = False
        if len(dataUser['password']) < 8:
            flash("La contraseña debe poseer al menos 8 caracteres")
            is_valid = False

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('schema_recipes').query_db(query, {
            "email": dataUser['email'],
        })

        if len(results) > 0:
            flash("La dirección de correo ya se encuentra registrada")
            is_valid = False

        return is_valid

    def __str__(self):
        return f"\
            first_name: {self.first_name} \n \
            last_name: {self.last_name}\n \
            email: {self.email}\n \
            created_at: {self.created_at}\n \
            updated_at: {self.updated_at}\n "