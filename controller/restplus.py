import logging

from flask_restplus import Api

import settings

log = logging.getLogger(__name__)

api = Api(version='1.0', title='book recommender',
          description='REST endpoints to modelling user data')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.info(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

