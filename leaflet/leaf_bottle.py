__author__ = 'user'

from bottle import route, run, template, static_file

@route('/data/<filename>')
def server_static(filename):
    return static_file(filename, root='data')

run(host='localhost', port=8080)