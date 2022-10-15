from flask_app.config.mysqlconnection import connectToMySQL

class Model:
    esquema = "schema_recipes"
    tabla = None

    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM {cls.tabla}"
        results = connectToMySQL(cls.esquema).query_db(query, {
            "table": cls.tabla
        })
        
        listResult = []
        for result in results:
            listResult.append( cls(result) )
        return listResult

    @classmethod
    def get_one(cls, id):
        query = f"SELECT * FROM {cls.tabla} WHERE id= %(id)s"
        results = connectToMySQL(cls.esquema).query_db(query, {
            "table": cls.tabla,
            "id": id
        })

        print("R:", results)

        return cls(results[0])

    @classmethod
    def delete_one(cls, id):
        query = f"DELETE FROM {cls.tabla} WHERE id= %(id)s"
        result = connectToMySQL(cls.esquema).query_db(query, {
            "table": cls.tabla,
            "id": id
        })

        return result