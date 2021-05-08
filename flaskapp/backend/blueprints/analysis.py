from flask import Blueprint, jsonify, request
import couchdb
from configuration.config import Config

bp = Blueprint('Read and configure analysis', __name__, url_prefix='/api/analysis')

couchdb = couchdb.Server(Config.COUCHDB_URL)
twitter = couchdb['twitter']

@bp.route('/', methods=['GET'])
def list_views():
  '''
  return all analysis (couchDB views)
  ---
  responses:
    200:
      description: A list of couchDB views definitions
      schema:
        type: array
        items:
          type: object
          properties:
            id:
              type: string
              description: The id of the view
            view:
              type: object
              description: The content of the view
              properties:
                map:
                  type: string
                  description: the mapper function
                reduce:
                  type: string
                  description: the reduce function, it can be `_sum`, `_count` or predefined javascript function. It can be omitted.
  '''
  views = twitter.resource.get_json('_design_docs')[2]
  res = []
  for item in views['rows']:
    doc = twitter.get(item['id'])
    view = doc.get('views') and doc.get('views').get('all')
    if not view:
      continue
    res.append({
      'id': item['id'].split('/')[1],
      'view': view,
    })
  return jsonify(res)

@bp.route('/<id>', methods=['PUT'])
def put_view(id):
  """
  Update a view
  ---
  consumes:
    - application/json
  parameters:
    - in: path
      name: id
      required: true
      type: string
      description: The id of the view
    - in: body
      description: The functions of the view
      required: true
      schema:
        type: object
        properties:
          map:
            type: string
            description: the mapper function
          reduce:
            type: string
            description: the reduce function, it can be `_sum`, `_count` or predefined javascript function. It can be omitted.
        example: |
          {
              "map": "function (doc) { emit(doc.author_id, 1); }",
              "reduce": "_count"
          }
  responses:
    200:
      description: Success
  """

  doc = twitter.get('_design/'+id)
  rev = doc['_rev']

  view = request.get_json()

  doc = {
    '_id': '_design/'+id,
    '_rev': rev,
    'views': {'all': view},
    "language": "javascript",
    "options": {"partitioned": False },
  }

  twitter.save(doc)
  return jsonify({
    'success': True
  })

@bp.route('/<id>/record', methods=['GET'])
def get_records(id):
  '''
  Get all records of a view by view id
  ---
  parameters:
    - in: path
      name: id
      required: true
      type: string
      description: The id of the view

  responses:
    200:
      description: The result of the view
      schema:
  '''
  res = list(twitter.view(id+'/all', group=True))
  return jsonify({
    'result': res
  })

@bp.route('/<id>', methods=['DELETE'])
def remove_view(id):
  '''
  Remove a view by id
  ---
  parameters:
    - in: path
      name: id
      required: true
      type: string
      description: The id of the view

  responses:
    200:
      description: Success
      schema:
  '''

  doc = twitter.get('_design/'+id)
  twitter.delete(doc)

  return jsonify({
    'success': True,
  })