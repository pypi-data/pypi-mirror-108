from .parser import CordyParser


class JsonApiParser(CordyParser):

    def _raw_load_json(self, req):
        return super()._raw_load_json(req).get('data', {}).get('attributes')


parser = JsonApiParser()
use_args = parser.use_args
use_kwargs = parser.use_kwargs
