from flask_restplus import Api



api = Api(version='1.0', title='Assignment2 Project API',
        description='The API of the backend of Assignment2 Project App')

@api.errorhandler
def default_error_handler(e):
return {
    'error': True,
    'message': str(e),
}