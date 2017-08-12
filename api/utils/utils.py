import base64
from django.http import HttpResponse


class HttpResponseNoContent(HttpResponse):
    status_code = 204

class HttpResponseCreated(HttpResponse):
    status_code = 201

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_date(DateString1c):
    '''fetch date from 1c date string representation
        <2016-08-30T00:00:00> => <2016-08-30>
    '''
    s, _ = DateString1c.split('T')
    return s

def encode64(string):
    bs = base64.b64encode(bytes(string, 'utf8'))
    return str(bs, 'utf8')

def getConfirmationLink(email, code, rootUrl):
    query = '?email={email}&code={code}'.format(email=email, code=code)
    encodeQuery = encode64(query)
    return '{url}/?emailConfirmation={query}'.format(url=rootUrl, query=encodeQuery)

