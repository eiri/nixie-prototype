from sanic import Sanic, exceptions
from sanic.response import text, empty
from sanic.views import HTTPMethodView

from nixie.api import Nixie, KeyError

class NixieRootView(HTTPMethodView):
  """View for Nixie root end-point"""

  def __init__(self, nx):
    self.nx = nx
    super().__init__()

  async def get(self, request):
    keys = self.nx.list()
    resp =  '\n'.join(keys)
    return text(resp)

  async def post(self, request):
    key = self.nx.create()
    return text(key, status=201)


class NixieCounterView(HTTPMethodView):
  """View for Nixie counter end-point"""

  def __init__(self, nx):
    self.nx = nx
    super().__init__()

  async def get(self, request, key):
    try:
      val = self.nx.read(key)
      return text(f'{val}')
    except KeyError as e:
      raise exceptions.NotFound(f'Not Found')

  async def head(self, request, key):
    if self.nx.exists(key):
      return empty()
    else:
      raise exceptions.NotFound(f'Not Found')

  async def post(self, request, key):
    try:
      new_val = self.nx.next(key)
      return text(f'{new_val}')
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
