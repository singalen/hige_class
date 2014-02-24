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
            return 'природная стена и скалы <br><br> ' \
                   '<center><img src="http://pohodushki.org/ru/reports/krasnodon-walls-and-volnuhino-quarry/images/krasnodon-walls-and-volnuhino-quarry-2483x640x480x0.jpg"/></center>'
        if self.type == '♦':
            return '<b>сурикаты</b><br><br> ' \
                   '<center> <img src="http://fotogaleri.ntvmsnbc.com/Assets/PhotoGallery/Pictures/0000164064.jpg"/></center>'
        return 'степь'

    def get_cell_string(self):
        return self.type

    def is_passable(self):
        return self.type not in ['=', '#']


class Player:
    def __init__(self):
        self.inventory = []
        self.grass = 0
        self.gold = 0


class Suricat:
    def __init__(self):
        self.x = 4
        self.y = 5

    def walking(self): # двигаем сурикатов
        step_x = random.randint(-1, 1)
        step_y = random.randint(-1, 1)
        self.x += step_x
        self.y += step_y


player = Player()
suricat = Suricat()
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
global_map[suricat.x][suricat.y].type = '♦'  # сурикаты


@route('/')
def index():
    return 'Добро пожаловать в матрицу! <a href="/at/0/0">Вход здесь</a>, выхода нет.'


@route('/at/<x>/<y>')
def index(x, y):
    global global_map, player, suricat
    map = '<center> Карта: </center> <br>'

    x = int(x)
    y = int(y)
    cell = global_map[x][y]

    page = "Вы находитесь в точке ({}, {}). Здесь {}. <hr/>".format(x, y, cell.get_cell_type()) + "<hr/>"

    # продажа трав
    if x == 0 and y == 0:
        if player.grass != 0:
            player.gold += player.grass * 2 # 2 золота за 1 травинку
            player.grass = 0
            page += "<br><b>Вы продали все травы<b></red><br>"

    # вывод ресурсов
    page += "<br><b>" + make_grass() + "</b><br>"
    page += "<br><b>У вас " + str(player.gold) + " золота</b><br>"
    page += "<b>У вас " + str(player.grass) + " трав</b><br>"

    # движение
    if x > 0:
        if global_map[x - 1][y].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на север</b></a>'.format(x - 1, y)
        else:
            page += '<br/>На севере {}'.format(global_map[x - 1][y].get_cell_type())
    if x < len(global_map) - 1:
        if global_map[x + 1][y].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на юг</b></a>'.format(x + 1, y)
        else:
            page += '<br/>На юге {}'.format(global_map[x + 1][y].get_cell_type())
    if y > 0 and global_map[x][y - 1].is_passable():
        if global_map[x][y - 1].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на запад</b></a>'.format(x, y - 1)
        else:
            page += '<br/>На западе {}'.format(global_map[x][y - 1].get_cell_type())
    if y < len(global_map[x]) - 1:
        if global_map[x][y + 1].is_passable():
            page += '<br/><a href="/at/{}/{}"><b>Идти на восток</b></a>'.format(x, y + 1)
        else:
            page += '<br/>На востоке {}'.format(global_map[x][y + 1].get_cell_type())

    # передвижение сурикатов
    suricat.walking()

    # map by Romanzi (Рома)
    for i in range(30):
        for j in range(30):
            if i == x and j == y:
                map += "☺"
            else:
                if i == suricat.x and j == suricat.y:
                    map += '♦'
                else:
                    map += global_map[i][j].get_cell_string()
            ####
        map += '<br>'
    page += '<pre><code><center>' + map + '</center></code></pre>' #вставляем карту
    page += '<b> Легенда карты: <br><br> ☺ - игрок <br> = - озеро<br> * - кусты<br> # - природная стена и скалы' \
            '<br> ♦ - сурикаты</b>'

    return page


def make_grass():
    global player
    if random.randint(0, 4) == 1:
        grass = random.randint(1, 5)
        player.grass += grass
        return "Вы нашли " + str(grass) + " полезных трав(у)(ы) (их можно продать на месте старта)"
    return "К сожалению, тут нет полезных предметов"


run(host='localhost', port=8080)