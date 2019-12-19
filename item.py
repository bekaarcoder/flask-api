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
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': F"An item with name {name} already exists."}, 400
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
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
