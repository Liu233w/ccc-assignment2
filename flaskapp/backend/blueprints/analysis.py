from flask import Blueprint, jsonify, request
import couchdb
from configuration.config import Config

bp = Blueprint('Read and configure analysis', __name__, url_prefix='/api/analysis')

couchdb = couchdb.Server(Config.COUCHDB_URL)
twitter = couchdb['twitter']

@bp.route('/', methods=['GET'])
def list_views():
  '''
  return all analysis
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
  Update an analysis
  :id the id
  body: {
    map: 'A function',
    reduce: '_count or _sum'
  }
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
  Get all records of an id
  '''
  res = list(twitter.view(id+'/all', group=True))
  return jsonify({
    'result': res
  })