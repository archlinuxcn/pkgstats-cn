import tornado.web
import yaml
try:
  from yaml import CLoader as Loader
  from yaml import CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

def load(src):
  return yaml.load(src, Loader=Loader)

def dump(data, stream=None, **kwargs):
  mykwargs = {
    'allow_unicode': True,
    'default_flow_style': False,
  }
  mykwargs.update(kwargs)
  return yaml.dump(data, stream=stream, Dumper=Dumper, **mykwargs)

class StatsHandler(tornado.web.RequestHandler):
  def initialize(self, store_path):
    self.store_path = store_path

  def put(self):
    data = self.request.body
    data = load(data)
    # CF or nginx
    ip = self.request.headers.get(
      'Cf-Connecting-IP',
      self.request.headers.get(
        'X-Forwarded-For',
        self.request.remote_ip,
      ).split(',')[-1]
    )

    data['ip'] = ip
    # TODO: address

    with open(os.path.join(self.store_path, data['UUID']), 'w') as f:
      dump(data, stream=f)
