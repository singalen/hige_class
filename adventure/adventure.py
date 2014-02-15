# coding=utf-8
import random
from bottle import route, run, template


class Cell:
    def __init__(self):
        self.type = ' '
        self.items = []
        self.actions = []
        self.mobs = []

    def get_cell_type(self):
        if self.type == ' ':
            return 'равнина'
        if self.type == '*':
            return 'кусты'
        if self.type == '=':
            return 'озеро'
        if self.type == '#':
            return 'стена'
        return 'чисто поле'

    def is_passable(self):
        return self.type not in ['=', '#']


class Player:
    def __init__(self):
        self.inventory = []


player = Player()
global_map = []
for i in range(10):
    global_map.append([Cell() for j in range(10)])

for i in range(10):
    global_map[random.randint(0, 9)][random.randint(0, 9)].type = '*'
for i in range(10):
    global_map[random.randint(0, 9)][random.randint(0, 9)].type = '#'


@route('/')
def index():
    return 'Добро пожаловать в матрицу! <a href="/at/0/0">Вход здесь</a>, выхода нет.'

@route('/at/<x>/<y>')
def index(x, y):
    global global_map

    x = int(x)
    y = int(y)
    cell = global_map[x][y]

    page = "Вы находитесь в точке ({}, {}). Здесь {}. <hr/>".format(x, y, cell.get_cell_type()) + \
        " Здесь есть: <hr/>" + \
        "ничего."

    if x > 0:
        if global_map[x-1][y].is_passable():
            page += '<br/><a href="/at/{:d}/{}">Идти на север</a>'.format(x-1, y)
        else:
            page += '<br/>На севере {}'.format(global_map[x-1][y].get_cell_type())
    if x < len(global_map)-1:
        if global_map[x+1][y].is_passable():
            page += '<br/><a href="/at/{}/{}">Идти на юг</a>'.format(x+1, y)
        else:
            page += '<br/>На юге {}'.format(global_map[x+1][y].get_cell_type())
    if y > 0 and global_map[x][y-1].is_passable():
        if global_map[x][y-1].is_passable():
            page += '<br/><a href="/at/{}/{}">Идти на запад</a>'.format(x, y-1)
        else:
            page += '<br/>На западе {}'.format(global_map[x][y-1].get_cell_type())
    if y < len(global_map[x])-1:
        if global_map[x][y+1].is_passable():
            page += '<br/><a href="/at/{}/{}">Идти на восток</a>'.format(x, y+1)
        else:
            page += '<br/>На востоке {}'.format(global_map[x][y+1].get_cell_type())

    return page

run(host='localhost', port=8080)