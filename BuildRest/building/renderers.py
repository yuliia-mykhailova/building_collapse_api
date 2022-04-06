import json
from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        token = data.get('tokens', None)

        if token is not None and isinstance(token, bytes):
            data['tokens']['access'] = token.decode('utf-8')

        return json.dumps(data)
