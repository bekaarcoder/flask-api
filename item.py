import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        item = self.find_by_name(name)

        if item:
            return {'message': 'Item already added'}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'message': 'An error occured'}, 500
        return {'message': 'Item added successfully'}, 201

    def delete(self, name):
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
            return {'message': 'Item Deleted'}

        return {'message': 'Item does not exists'}, 400

    def put(self, name):
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            data = Item.parser.parse_args()
            updated_item = {'name': name, 'price': data['price']}
            query = "UPDATE items SET price=? WHERE name=?"
            cursor.execute(query, (updated_item['price'], name))

            connection.commit()
            connection.close()
            return updated_item

        return {'message': 'Item not found'}, 400

class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        items = []
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        for row in result:
            items.append({'_id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}
