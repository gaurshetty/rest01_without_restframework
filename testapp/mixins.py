from django.core.serializers import serialize
from django.http import HttpResponse
import json


class HttpResponseMixin(object):
    def render_to_httpresponse(self, data, status=200):
        return HttpResponse(data, content_type='application/json', status=status)


class SerializeMixin(object):
    def serialize(self, qs):
        json_data = serialize('json', qs)
        pdict = json.loads(json_data)
        final_list = []
        for obj in pdict:
            emp_data = obj['fields']
            final_list.append(emp_data)
        json_data = json.dumps(final_list)
        return json_data
