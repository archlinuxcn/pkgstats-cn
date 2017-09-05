import tornado.web
import yaml
try:
  from yaml import CLoader as Loader
  from yaml import CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

def load(src):
  return yaml.load(src, Loader=Loader)

class StatsHandler(tornado.web.RequestHandler):
  def put(self):
    data = self.request.body
    data = load(data)
    # CF or nginx
    ip = self.request.headers.get(
      'Cf-Connecting-IP',
      self.request.headers['X-Forwarded-For'].split(',')[0]
    )

    # TODO: store data
