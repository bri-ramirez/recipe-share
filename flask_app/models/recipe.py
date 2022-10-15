import datetime

from flask import flash, session
from flask_app.models.models import Model
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Recipe(Model):
    tabla = "recipes"

    def __init__( self , data ):
        
        if 'id' in data:
            self.id = data['id']
        
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.user_id = data['user_id']
        
        if 'created_at' in data:
            self.created_at = data['created_at']
        
        if 'updated_at' in data:
            self.updated_at = data['updated_at']

        if 'user' in data:
            self.user = data['user']

    @staticmethod
    def isValid(dataUser):
        is_valid = True

        if len(dataUser['name']) < 5:
            flash("El nombre debe poseer al menos 5 caracteres")
            is_valid = False
        if len(dataUser['description']) < 5:
            flash("La descripción debe poseer al menos 5 caracteres")
            is_valid = False
        if len(dataUser['instructions']) < 5:
            flash("Las instrucciones deben poseer al menos 5 caracteres")
            is_valid = False
        if len(dataUser['date_made']) == '':
            flash("La fecha es requerida")
            is_valid = False
            
        return is_valid

    @classmethod
    def save(cls, data):
        query = f"INSERT INTO {cls.tabla} ( name, description, instructions, date_made, under, user_id ) VALUES ( %(name)s , %(desc)s , %(inst)s, %(datem)s, %(under)s, %(user_id)s );" 
        return connectToMySQL(cls.esquema).query_db( query, data )

    @classmethod
    def update(cls, data):
        query = f"UPDATE {cls.tabla} SET name = %(name)s, description = %(desc)s , instructions = %(inst)s, date_made = %(datem)s, under = %(under)s, updated_at = %(updated)s WHERE id = %(id)s;"
        
        # agregamos un key nuevo al diccionario
        data.update({
            "updated": datetime.datetime.now()
        })

        return connectToMySQL(cls.esquema).query_db( query, data )

    @classmethod
    def getWithUsers(cls):
        query = f"SELECT * FROM recipes \
            JOIN users ON recipes.user_id = users.id;"
        
        results = connectToMySQL(cls.esquema).query_db(query)


        listResult = []
        for result in results:
            
            user_data = {
                'id': result["users.id"],
                'first_name': result["first_name"],
                'last_name': result["last_name"],
                'email': result["email"],
                'password': result["password"],
                'created_at': result["users.created_at"],
                'updated_at': result["users.updated_at"],
            }

            result['user'] = User(user_data)
            listResult.append( cls(result) )
        return listResult

    @classmethod
    def getOneWithUser(cls, recipeId):
        query = f"SELECT * FROM recipes \
            JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        
        results = connectToMySQL(cls.esquema).query_db(query, {
            'id': recipeId
        });
        
        result = results[0]
            
        user_data = {
            'id': result["users.id"],
            'first_name': result["first_name"],
            'last_name': result["last_name"],
            'email': result["email"],
            'password': result["password"],
            'created_at': result["users.created_at"],
            'updated_at': result["users.updated_at"],
        }

        result['user'] = User(user_data)
        return cls(result)