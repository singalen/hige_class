# coding=utf-8
import random
from bottle import route, run, template

global_map = []
for i in range(10):
    global_map.append([' ' for j in range(10)])

for i in range(10):
    global_map[random.randint(0, 9)][random.randint(0, 9)] = '*'

@route('/')
def index():
    return 'Добро пожаловать в матрицу! <a href="/at/0/0">Вход здесь</a>, выхода нет.'


def get_cell_type(cell):
    if cell == ' ':
        return 'равнина'
    if cell == '*':
        return 'кусты'
    return 'чисто поле'


@route('/at/<x>/<y>')
def index(x, y):
    global global_map

    x = int(x)
    y = int(y)
    cell = global_map[x][y]

    page = "Вы находитесь в точке ({}, {}). Здесь {}. <hr/>".format(x, y, get_cell_type(cell)) + \
        " Здесь есть: <hr/>" + \
        "ничего."

    if x > 0:
        page += '<br/><a href="/at/{:d}/{}">Идти на север</a>'.format(x-1, y)
    if x < len(global_map)-1:
        page += '<br/><a href="/at/{}/{}">Идти на юг</a>'.format(x+1, y)
    if y > 0:
        page += '<br/><a href="/at/{}/{}">Идти на запад</a>'.format(x, y-1)
    if x < len(global_map[x])-1:
        page += '<br/><a href="/at/{}/{}">Идти на восток</a>'.format(x, y+1)

    return page

run(host='localhost', port=8080)