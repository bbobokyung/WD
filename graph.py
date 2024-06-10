import matplotlib as mpl
mpl.use('Agg')

from cgi import parse_qs
from template import html
import matplotlib.pyplot as plt
import os

def application(environ, start_response):
    if environ['PATH_INFO'] == '/img/graph.png':
        try:
            with open('./img/graph.png', 'rb') as f:
                response_body = f.read()
        except Exception as e:
            response_body = b''
            print(f"Error: {e}")
        start_response('200 OK', [
            ('Content-Type', 'image/png'),
            ('Content-Length', str(len(response_body)))
        ])
        return [response_body]
    else:
        d = parse_qs(environ['QUERY_STRING'])
        a = d.get('a', [''])[0]
        b = d.get('b', [''])[0]
        c = d.get('c', [''])[0]
        if '' not in [a, b, c]:
            try:
                a, b, c = int(a), int(b), int(c)
                x = [n / 10.0 for n in range(-40, 41)]
                y = [a * n ** 2 + b * n + c for n in x]
                fig = plt.figure()
                plt.plot(x, y)
                plt.grid()
                if not os.path.exists('./img'):
                    os.makedirs('./img')
                fig.savefig('./img/graph.png')
                plt.close(fig)
            except ValueError:
                pass
        response_body = html
        start_response('200 OK', [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))
        ])
        return [response_body]
