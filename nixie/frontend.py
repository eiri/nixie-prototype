from flask import Flask, Response, request
from nixie.core import Nixie

class Frontend:
  """REST frontend"""

  def __init__(self):
    self.nx = Nixie()
    self.app = Flask(__name__.split('.')[0])
    self.__set_rules()
    return None

  def run(self, port=7312, debug=False):
    self.app.run(port=port, debug=debug)

  def __set_rules(self):
    self.app.add_url_rule('/', 'list', self.list)
    self.app.add_url_rule('/', 'create', self.create, methods=['POST'])
    self.app.add_url_rule('/<key>', 'exists', self.exists, methods=['HEAD'])
    self.app.add_url_rule('/<key>', 'read', self.read)
    self.app.add_url_rule('/<key>/incr', 'incr', self.incr, methods=['PUT'])
    self.app.add_url_rule('/<key>/incr/<val>', 'incr_val', self.update,
      methods=['PUT'])
    self.app.add_url_rule('/<key>/decr', 'decr', self.decr, methods=['PUT'])
    self.app.add_url_rule('/<key>/decr/<val>', 'decr_val', self.update,
      methods=['PUT'])
    self.app.add_url_rule('/<key>/<val>', 'put', self.put, methods=['PUT'])
    self.app.add_url_rule('/<key>', 'delete', self.delete, methods=['DELETE'])

  """CRUD"""
  def create(self):
    key = self.nx.create()
    return Response(key, status=201, mimetype='text/plain')

  def read(self, key):
    val = self.nx.read(key)
    if val is None:
      return Response('', status=404, mimetype='text/plain')
    else:
      resp = str(val)
      return Response(resp, status=200, mimetype='text/plain')

  def update(self, key, val):
    try:
      if request.url_rule.endpoint == 'decr_val':
        val = '-' + val
      new_val = self.nx.update(key, val)
      resp = str(new_val)
      return Response(resp, status=200, mimetype='text/plain')
    except KeyError as e:
      return Response(e, status=404, mimetype='text/plain')
    except ValueError as e:
      return Response(e, status=400, mimetype='text/plain')

  def delete(self, key):
    try:
      self.nx.delete(key)
      return Response('', status=204, mimetype='text/plain')
    except KeyError as e:
      return Response(e, status=404, mimetype='text/plain')

  """extra"""
  def exists(self, key):
    if self.nx.exists(key):
      return Response('', status=200, mimetype='text/plain')
    else:
      return Response('', status=404, mimetype='text/plain')

  def list(self):
    keys = self.nx.list()
    resp =  '\n'.join(keys)
    return Response(resp, mimetype='text/plain')

  def put(self, key, val):
    try:
      new_val = self.nx.put(key, val)
      resp = str(new_val)
      return Response(resp, status=200, mimetype='text/plain')
    except KeyError as e:
      return Response(e, status=404, mimetype='text/plain')
    except ValueError as e:
      return Response(e, status=400, mimetype='text/plain')

  def incr(self, key):
    try:
      new_val = self.nx.incr(key)
      resp = str(new_val)
      return Response(resp, status=200, mimetype='text/plain')
    except KeyError as e:
      return Response(e, status=404, mimetype='text/plain')

  def decr(self, key):
    try:
      new_val = self.nx.decr(key)
      resp = str(new_val)
      return Response(resp, status=200, mimetype='text/plain')
    except KeyError as e:
      return Response(e, status=404, mimetype='text/plain')


  # def put(self, key, value):
  #   self.__validate_key_value(key, value)
  #   self.storage[key] = int(value)
  #   return self.storage[key]
