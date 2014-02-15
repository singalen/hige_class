# coding=utf-8
from bottle import route, run, template

request_count = 0

@route('/hello/<name>')
def index(name):
    global request_count
    request_count += 1
    return template('<b>Привет, {{name}}</b>!', name=name)

@route('/')
def root():
    global request_count
    request_count += 1
    return "Сервер обработал {0} запрос(а)(ов)(ыч)".format(request_count)

run(host='localhost', port=8080)