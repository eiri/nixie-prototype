from sanic import Sanic, exceptions
from sanic.response import text, empty
from sanic.views import HTTPMethodView

from nixie.api import Nixie, KeyError

class FrontendHelper:
  def get_headers(self, key):
    meta = self.nx.read_meta(key)
    headers = {'nixie-step': meta['step']}
    if meta['name'] is not None:
      headers['nixie-name'] = meta['name']
    if meta['description'] is not None:
      headers['nixie-description'] = meta['description']
    return headers

  def get_meta(self, request):
    start, step, name, description = 0, 1, None, None
    if request.body != b'':
      start = int(request.body)
    if 'nixie-step' in request.headers:
      step = int(request.headers['nixie-step'])
    if 'nixie-name' in request.headers:
      name = request.headers['nixie-name']
    if 'nixie-description' in request.headers:
      description = request.headers['nixie-description']
    return (start, step, name, description)


class NixieRootView(HTTPMethodView, FrontendHelper):
  """View for Nixie root end-point"""

  def __init__(self, nx):
    self.nx = nx
    super().__init__()

  async def get(self, request):
    keys = self.nx.list()
    resp =  '\n'.join(keys)
    return text(resp)

  async def post(self, request):
    (start, step, name, description) = self.get_meta(request)
    key = self.nx.create(start, step, name, description)
    headers = self.get_headers(key)
    return text(key, status=201, headers=headers)


class NixieCounterView(HTTPMethodView, FrontendHelper):
  """View for Nixie counter end-point"""

  def __init__(self, nx):
    self.nx = nx
    super().__init__()

  async def get(self, request, key):
    try:
      val = self.nx.read(key)
      headers = self.get_headers(key)
      return text(f'{val}', headers=headers)
    except KeyError as e:
      raise exceptions.NotFound(f'Not Found')

  async def head(self, request, key):
    if self.nx.exists(key):
      headers = self.get_headers(key)
      return empty(headers=headers)
    else:
      raise exceptions.NotFound(f'Not Found')

  async def post(self, request, key):
    try:
      new_val = self.nx.next(key)
      headers = self.get_headers(key)
      return text(f'{new_val}', headers=headers)
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')

  async def patch(self, request, key):
    try:
      (_, step, name, description) = self.get_meta(request)
      self.nx.update_meta(key, step, name, description)
      headers = self.get_headers(key)
      return empty(headers=headers)
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')

  async def delete(self, request, key):
    try:
      self.nx.delete(key)
      return empty()
    except KeyError as e:
      raise exceptions.NotFound(f'{e}')


class Frontend:
  """REST frontend"""

  def __init__(self):
    self.nx = Nixie()
    self.app = Sanic(__name__.split('.')[0])
    self.app.config.FALLBACK_ERROR_FORMAT = "text"
    self.app.add_route(NixieRootView.as_view(self.nx), "/")
    self.app.add_route(NixieCounterView.as_view(self.nx), "/<key:string>")
    return None

  def run(self, port=7312, debug=False):
    self.app.run(port=port, debug=debug)
