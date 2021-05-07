from ..api import api
from flask_restplus import Resource, fields

ns = api.namespace('example', description='Examples of how to write apis')

@ns.route('/')
class GetPostExample(Resource)
  postInput = ns.model('PostInput', {
    "int": fields.Integer(description='Integer input', required=True),
    "str": fields.String(description='String input', required=True),
  })
  postOutput = ns.model('PostOutput', {
    ''
  })

  getInput = ns.model('GetInput', {
    'id': fields.Integer,
  })

  @api.expect(postInput)
  @api.
