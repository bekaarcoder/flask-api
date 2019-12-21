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

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[1], 'price': row[2]}}
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(select_query, (name,))
        row = result.fetchone()
        if row:
            return {'message': 'Item already added'}, 400

        data = Item.parser.parse_args()
        query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(query, (name, data['price']))
        connection.commit()
        connection.close()
        return {'message': 'Item added successfully'}, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item Deleted'}

    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            return {'message': 'Item not found'}, 404
        # data = request.get_json()
        data = Item.parser.parse_args()
        item.update(data)
        return item

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
