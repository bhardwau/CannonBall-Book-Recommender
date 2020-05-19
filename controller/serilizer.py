from flask_restplus import fields
from controller.restplus import api

book = api.model('Book',
{
   "_id":fields.String(desctiption = 'book id gen by mongo'),
   "bookID":fields.Integer(description = 'book id gen by good reads'),
   "title":fields.Raw(description = 'book title'),
   "authors":fields.String(description = 'book authors'),
   "average_rating":fields.Float(dedscription = 'rating'),
   "isbn":fields.String(dedscription = 'isbn'),
   "isbn13":fields.Integer(dedscription = 'isbn 14'),
   "language_code":fields.String(dedscription = 'language code'),
   "# num_pages":fields.Integer(dedscription = 'page number'),
   "ratings_count":fields.Integer(dedscription = 'rating count'),
   "text_reviews_count":fields.Integer(dedscription = 'text review count'),
   "user_id":fields.String(desctiption = 'book id gen by mongo'),
   "user":fields.Nested(
      api.model('user', {
         "_id": fields.String(desctiption='book id gen by mongo'),
         "name": fields.String(desctiption='user name'),
         "address": fields.String(desctiption='address'),
         "job": fields.String(desctiption='job')
      })
   )
})
