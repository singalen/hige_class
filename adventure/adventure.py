# coding=utf-8
import random
from bottle import route, run, template, request, static_file


class Cell:
    def __init__(self):
        self.type = '_'
        self.items = []
        self.actions = []
        self.mobs = []

    def get_cell_type(self):
        if self.type == '_':
            return template('степь <br><br> ' \
                            '<center><img src="/images/{{img}}"/> </center>', img='step.jpg')
        if self.type == '*':
            return template('кусты <br><br> ' \
                            '<center><img src="/images/{{img}}"/> </center>', img='bush.jpg')
        if self.type == '=':
            return template('озеро <br><br> ' \
                            '<center><img src="/images/{{img}}"/> </center>', img='lake.jpg')
        if self.type == '#':
            return template('природная стена и скалы <br><br> ' \
                            '<center><img src="/images/{{img}}"/></center>', img='wall.jpg')
        if self.type == '♦':
            return template('находятся <b>сурикаты</b><br><br> ' \
                            '<center> <img src="/images/{{img}}"/>' \
                            '<br><form method="POST" action="/health"><input type="submit" name="submit" value="Пополнить здоровье"></form>' \
                            '<br><form method="POST" action="/maxhealth"><input type="submit" name="submit" value="Купить зелье для повышения здоровья"></form></center>', img='suricat.jpg')
        if self.type == '&':
            return template('находятся <b>змеи</b>, они хотят напасть на Вас. Примите бой с честью.' \
                            '<center><img src="/images/{{img}}"/>' \
                            '<br><form method="POST" action="/battle"><input type="submit" name="submit" value="Удар!"></form>', img='snake.jpg')
        return 'степь'

    def get_cell_string(self):
        return self.type

    def is_passable(self):
        return self.type not in ['=', '#']


class Player:
    def __init__(self):
        self.inventory = []
        self.health = 30
        self.max_health = 30
        self.attack = 5
        self.grass = 0
        self.gold = 0
        self.x = 0
        self.y = 0

    def attacking(self):
        power = random.randint(0, self.attack)
        return power


class Suricat:
    def __init__(self):
        self.x = 4
        self.y = 5

    def walking(self): # двигаем сурикатов
        step_x = random.randint(-1, 1)
        step_y = random.randint(-1, 1)
        self.x += step_x
        self.y += step_y


class Snake:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.health = 30
        self.max_health = 30
        self.attack = 4

    def attacking(self):
        power = random.randint(0, self.attack)
        return power


player = Player()
suricat = Suricat()
snake = Snake()
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
global_map[snake.x][snake.y].type = '&' # змеи


@route('/')
def index():
    return 'Добро пожаловать в матрицу! <a href="/at/1/1">Вход здесь</a>, выхода нет. <br>' \
                    'Собирайте и продавайте полезные травы, сражайтесь со змеями и торгуйте с сурикатами!'


@route('/health', method='POST')
def health():
    global player
    if player.gold > 10 and player.health < 30:
        player.gold -= 10
        player.health = player.max_health
        return 'Вы были вылечены сурикатами за <b>10</b> золота<br><br>' + index(player.x, player.y)
    else:
        return 'У вас должно быть <b>10</b> золота для этого или вы здоровы<br><br>' + index(player.x, player.y)

@route('/maxhealth', method='POST')
def maxhealth():
    global player
    if player.gold > 20:
        player.gold -= 20
        player.max_health = 50
        player.health = player.max_health
        return 'Вы купили у сурикатов зелье, которое увеличило вашу мощь за 20 золота' + index(player.x, player.y)
    else:
        return 'У вас должно быть 20 золота для этого' + index(player.x, player.y)



@route('/battle', method='POST')
def battle():
    global player, snake, global_map
    s_attack = snake.attacking()
    p_attack = player.attacking()
    player.health = player.health - s_attack
    snake.health = snake.health - p_attack
    if snake.health < 1:
        player.gold += 20
        global_map[snake.x][snake.y].type = '_'
        return '<b>Поздравляю, Вы победили! И за победу получаете 20 золота!</b><br><br>' + index(snake.x, snake.y)
    if player.health < 1:
        player.gold = 0
        player.grass = 0
        player.health = 2
        return '<b>Увы, но Вы проиграли. Но вы выижили и потеряли все свои деньги.</b><br><br>' + index(snake.x,
                                                                                                        snake.y)
    return 'Здоровье: <b> ' + str(player.health) + '/' + str(player.max_health) + '\
           </b>      Золото: <b> ' + str(player.gold) + '</b>      Травы: <b>' + str(player.grass) + \
           '<center><img src="http://www.xakac.info/sites/default/files/d21c50880735.jpg?1290479818"/>' \
           '<br><form method="POST" action="/battle"><input type="submit" name="submit" value="Удар!"></form></center>' \
           '<br> <center><b>Вы нанесли ' + str(p_attack) + ' урона. <br> Враг нанёс ' + str(
        s_attack) + ' урона.</center> </b>'


@route('/at/<x>/<y>')
def index(x, y):
    global global_map, player, suricat, snake
    map = '<center> Карта: </center> <br>'

    x = int(x)
    y = int(y)
    cell = global_map[x][y]
    player.x = x
    player.y = y

    page = "Здоровье: <b>" + str(player.health) + "/" + str(player.max_health) + \
           "</b>      Золото: <b>" + str(player.gold) + "</b>      Травы: <b>" + str(player.grass)
    page += "</b><br> Вы находитесь в точке ({}, {}). Здесь {}. <hr/>".format(x, y, cell.get_cell_type()) + "<hr/>"

    # продажа трав
    if x == 0 and y == 0:
        if player.grass != 0:
            player.gold += player.grass * 2 # 2 золота за 1 травинку
            player.grass = 0
            page += "<br><b>Вы продали все травы<b></red><br>"

    # вывод травы
    page += "<br><b>" + make_grass() + "</b><br>"

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
        map += '<br>'
    page += '<pre><code><center>' + map + '</center></code></pre>' #вставляем карту
    page += '<b> Легенда карты: <br><br> ☺ - игрок <br> = - озеро<br> * - кусты<br> # - природная стена и скалы' \
            '<br> ♦ - сурикаты <br> & - змеи</b>'

    return page


def make_grass():
    global player
    if random.randint(0, 4) == 1:
        grass = random.randint(1, 5)
        player.grass += grass
        return "Вы нашли " + str(grass) + " полезных трав(у)(ы) (их можно продать на месте старта)"
    return "К сожалению, тут нет полезных предметов"


@route("/images/<filename>")
def getImg(filename):
    return static_file(filename, root='images')


run(host='localhost', port=8080, quiet=False)