import json
import random
import zanryu
import classroom
import report
import pe

from gevent import pywsgi, sleep
from geventwebsocket.handler import WebSocketHandler

def webSocketApp(environ, start_response):
    ws = environ['wsgi.websocket']
    while True:
        data = ws.receive()
        #if data is None:
        #    break
		# process the data, i.e. print it:
        result = {}
        data = json.loads(data);
        print data['app']
        app = data['app']
        if app == 'zanryu':
            result = zanryu.zanryu(data['building'], data['floor'], data['room'], data['login'], data['pass'])
        elif app == 'classroom':
            result = classroom.classroom(data['day'], data['period'], data['login'], data['pass'])
        elif app == 'report':
            result = report.report(data['login'], data['pass'])
        else:
            result = pe.pe(data['year'], data['month'], data['day'], data['sport'], data['period'], data['login'], data['pass']) 
#            result = data
        print result
        ws.send(result)

server = pywsgi.WSGIServer(("", 8080), webSocketApp,
    handler_class=WebSocketHandler)
server.serve_forever()
