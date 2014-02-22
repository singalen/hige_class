# coding=utf-8
import random
from bottle import route, run, template


class Cell:
    def __init__(self):
        self.type = '_'
        self.items = []
        self.actions = []
        self.mobs = []

    def get_cell_type(self):
        if self.type == '_':
            return 'равнина <br><br> ' \
                   '<center><img src="http://images2.wikia.nocookie.net/__cb20080409130942/starwars/images/f/f1/Great_Grass_Plains.jpg"/> </center>'
        if self.type == '*':
            return 'кусты <br><br> ' \
                   '<center><img src="http://nature.baikal.ru/phs/norm/10/10250.jpg"/> </center>'
        if self.type == '=':
            return 'озеро <br><br> ' \
                   '<center><img src="http://stat18.privet.ru/lr/0b1c4dfd0bf718666448823c8401546c"/> </center>'
        if self.type == '#':
            return 'стена <br><br> ' \
                      '<center><img src="http://pohodushki.org/ru/reports/krasnodon-walls-and-volnuhino-quarry/images/krasnodon-walls-and-volnuhino-quarry-2483x640x480x0.jpg"/></center>'
        return 'чисто поле'
    def get_cell_string(self):
        return self.type

    def is_passable(self):
        return self.type not in ['=', '#']


class Player:
    def __init__(self):
        self.inventory = []
        self.grass = 0


player = Player()
global_map = []
for i in range(30):
    global_map.append([Cell() for j in range(30)])

for i in range(10):
    x = random.randint(0, 29)
    y = random.randint(0, 29)
    global_map[x][y].type = '*'
for i in range(10):
    x = random.randint(0, 29)
    y = random.randint(0, 29)
    global_map[x][y].type = '#'
for i in range(10):
    x = random.randint(0, 29)
    y = random.randint(0, 29)
    global_map[x][y].type = '='

@route('/')
def index():
    return 'Добро пожаловать в матрицу! <a href="/at/0/0">Вход здесь</a>, выхода нет.'

@route('/at/<x>/<y>')
def index(x, y):
    global global_map, player
    map = '<center> Карта: </center> <br>'

    x = int(x)
    y = int(y)
    cell = global_map[x][y]

    page = "Вы находитесь в точке ({}, {}). Здесь {}. <hr/>".format(x, y, cell.get_cell_type()) + "<hr/>"
    page += "<br><b>" + makeGrass() + "</b><br>"
    page += "<b>У вас " + str(player.grass) + " трав</b><br>"

    # движение
    if x > 0:
        if global_map[x-1][y].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на север</b></a>'.format(x-1, y)
        else:
            page += '<br/>На севере {}'.format(global_map[x-1][y].get_cell_type())
    if x < len(global_map)-1:
        if global_map[x+1][y].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на юг</b></a>'.format(x+1, y)
        else:
            page += '<br/>На юге {}'.format(global_map[x+1][y].get_cell_type())
    if y > 0 and global_map[x][y-1].is_passable():
        if global_map[x][y-1].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на запад</b></a>'.format(x, y-1)
        else:
            page += '<br/>На западе {}'.format(global_map[x][y-1].get_cell_type())
    if y < len(global_map[x])-1:
        if global_map[x][y+1].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на восток</b></a>'.format(x, y+1)
        else:
            page += '<br/>На востоке {}'.format(global_map[x][y+1].get_cell_type())

    # map by Romanzi (Рома)
    for i in range(30):
        for j in range(30):
            if i == x and j == y:
                map += "☺"
            else:
                map += global_map[i][j].get_cell_string()
        map += '<br>'
    page += '<pre><code><center>' + map + '</center></code></pre>' #пробуем вставить карту
    return page

def makeGrass():
    global player
    if(random.randint(0, 4) == 1):
        grass = random.randint(1, 5)
        player.grass += grass
        return "Вы нашли " + str(grass) + "полезных трав(у)(ы)"
    return "К сожалению, тут нет полезных предметов"


run(host='localhost', port=8080)