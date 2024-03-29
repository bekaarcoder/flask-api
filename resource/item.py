import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return {'message': 'Item already added'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured'}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
            # connection = sqlite3.connect('data.db')
            # cursor = connection.cursor()
            #
            # query = "DELETE FROM items WHERE name=?"
            # cursor.execute(query, (name,))
            #
            # connection.commit()
            # connection.close()

        return {'message': 'Item does not exists'}, 400

    def put(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            data = Item.parser.parse_args()
            item.price = data['price']
            item.save_to_db()
            return item.json()
            # connection = sqlite3.connect('data.db')
            # cursor = connection.cursor()
            #
            # data = Item.parser.parse_args()
            # updated_item = {'name': name, 'price': data['price']}
            # query = "UPDATE items SET price=? WHERE name=?"
            # cursor.execute(query, (updated_item['price'], name))
            #
            # connection.commit()
            # connection.close()

        return {'message': 'Item not found'}, 400

class Items(Resource):
    def get(self):
        items = ItemModel.query.all()
        item_list = []
        for item in items:
            item_list.append(item.json())
        return {'items': item_list}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # items = []
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # for row in result:
        #     items.append({'_id': row[0], 'name': row[1], 'price': row[2]})
        # connection.close()
