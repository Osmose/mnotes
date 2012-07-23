import json

from django.http import HttpResponse


def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON '
                        'serializable' % (type(obj), repr(obj)))


class JSONResponse(HttpResponse):
    def __init__(self, data, status=200):
        data_json = json.dumps(data, default=handler)
        super(JSONResponse, self).__init__(data_json,
                                           mimetype='application/json',
                                           status=status)


class JSONPResponse(HttpResponse):
    def __init__(self, data):
        data_json = json.dumps(data, default=handler)
        response_body = 'mnotes.handleResponse(%s)' % data_json
        super(JSONPResponse, self).__init__(response_body,
                                           mimetype='text/javascript')
