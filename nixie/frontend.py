from sanic import Sanic, exceptions
from sanic.response import text, empty
from nixie.core import Nixie, KeyError

class Frontend:
  """REST frontend"""

  def __init__(self):
    self.nx = Nixie()
    self.app = Sanic(__name__.split('.')[0])
    self.app.config.FALLBACK_ERROR_FORMAT = "text"
    self.__set_rules()
    return None

  def run(self, port=7312, debug=False):
    self.app.run(port=port, debug=debug)

  def __set_rules(self):
    self.app.add_route(self.list, '/', methods=['GET'])
    self.app.add_route(self.create, '/', methods=['POST'], )
    self.app.add_route(self.exists, '/<key>', methods=['HEAD'])
    self.app.add_route(self.read, '/<key>', methods=['GET'])
    # self.app.add_route(self.put, '/<key:string>/<val:int>', methods=['PUT'])
    self.app.add_route(self.incr, '/<key>/incr', methods=['PUT'])
    self.app.add_route(self.decr, '/<key>/decr', methods=['PUT'])
    self.app.add_route(self.update, '/<key>/incr/<val:int>', methods=['PUT'])
    self.app.add_route(self.update, '/<key>/decr/<val:int>', methods=['PUT'])
    self.app.add_route(self.delete, '/<key>', methods=['DELETE'])

  """CRUD"""
  async def create(self, request):
    key = self.nx.create()
    return text(key, status=201)

  async def read(self, request, key):
    val = self.nx.read(key)
    if val is None:
      raise exceptions.NotFound(f'Not Found')
    else:
      return text(f'{val}')

  async def update(self, request, key, val):
    try:
      if 'decr' in request.path:
        val = -1 * val
      new_val = self.nx.update(key, val)
      return text(f'{new_val}')
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')
    except ValueError as e:
      raise exceptions.InvalidUsage(f'{e}')

  async def delete(self, request, key):
    try:
      self.nx.delete(key)
      return empty()
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')

  """extra"""
  async def exists(self, request, key):
    if self.nx.exists(key):
      return empty()
    else:
      raise exceptions.NotFound(f'Not Found')

  async def list(self, request):
    keys = self.nx.list()
    resp =  '\n'.join(keys)
    return text(resp)

  async def put(self, request, key, val):
    try:
      new_val = self.nx.put(key, val)
      return text(f'{new_val}')
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')
    except ValueError as e:
      raise exceptions.InvalidUsage(f'{e}')

  async def incr(self, request, key):
    try:
      new_val = self.nx.incr(key)
      return text(f'{new_val}')
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')

  async def decr(self, request, key):
    try:
      new_val = self.nx.decr(key)
      return text(f'{new_val}')
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')
