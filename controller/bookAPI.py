from flask_restplus import Resource
from controller.restplus import api
from model.data_model import get_books_and_users,train_model
from controller.serilizer import book
namespace = api.namespace('v1/books', description = 'books controller',ordered=False)

@namespace.route('/book')
class BookAPI(Resource):

    def get(self):
        book_list,_ = get_books_and_users()
        return book_list

@namespace.route('/train')
class TrainModel(Resource):
    def get(self):
        return train_model('popularity')