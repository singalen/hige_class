# coding=utf-8
import random
from bottle import route, run, template

# http://www.old-games.ru/forum/showthread.php?t=51838
# http://leonid.shevtsov.me/ru/monsterland-article

# global_map = None


class Cell:
    def __init__(self, description, x, y):
        self.description = description
        self.items = []
        self.gold = 0
        self.x = x
        self.y = y

    def __str__(self):
        return self.description

    def on_enter(self, player):
        if self.gold > 0:
            player.gold += self.gold
            result = 'Вы нашли {} золота!'.format(self.gold)
            self.gold = 0
            return result
        return ''

    def actions(self, player):
        return dict()

    def is_passable(self, player):
        return True

    def with_gold(self, gold):
        self.gold = gold
        return self

    def with_thing(self, item):
        self.items.append(item)
        return self


class PlainsCell(Cell):
    def __init__(self, x, y, n):
        super().__init__('Чисто поле', x, y)

    def on_enter(self, player):
        player.strength -= 0.01
        return super().on_enter(player)


class MonsterCell(PlainsCell):
    def __init__(self, x, y, n):
        super().__init__(x, y, n)
        self.description = 'Чудовище!'
        self.monster_gold = n % 10
        self.strength = (n // 10) * 3

    def actions(self, player):
        actions = [
            {'id': 'fight', 'name': 'Сражаться'},
        ]
        if ThingTypes.HELMET in player.inventory:
            actions.append({'id': 'hide', 'name': 'спрятаться под Шлемом'})
        else:
            actions.append({'id': 'escape', 'name': 'Сбежать'})
        return actions

    def on_enter(self, player):
        return super().on_enter(player)


class SwampCell(PlainsCell):
    def __init__(self, x, y, n):
        super().__init__('Болото', x, y)


class WaterCell(Cell):
    def __init__(self, x, y, n):
        super().__init__('Вода' if n != 179 else 'Мелководье', x, y)

    def is_passable(self, player):
        return ThingTypes.BOAT in player.inventory


class RockCell(Cell):
    def __init__(self, x, y, n):
        super().__init__('Скалы', x, y)

    def is_passable(self, player):
        return ThingTypes.BOMB in player.inventory

    def on_enter(self, player):
        # Пока не будем "случайно биться".
        # if ThingTypes.COAT not in player.inventory:
        #     player.strength -= 0.5
        result = super().on_enter(player)

        if ThingTypes.BOMB in player.inventory:
            global_map[self.x][self.y] = PlainsCell(111, self.x, self.y)
            result += '<br/>Вы взорвали скалу бомбой!' + global_map[self.x][self.y].on_enter(player)
        return result


def cell_factory(x, y, n):
    if 182 <= n <= 200:
        return RockCell(x, y, n)
    if 179 <= n <= 181:
        return WaterCell(x, y, n).with_gold(1 if n == 181 else 0)
    if 171 <= n <= 178:
        return SwampCell(x, y, n)
    if ThingTypes.FIRST <= n <= ThingTypes.LAST:
        return PlainsCell(x, y, n).with_thing(n)
    if 10 <= n <= 109:
        return MonsterCell(x, y, n)

    return PlainsCell(x, y, n).with_gold(1 if n == 130 or random.randint(0, 7) == 7 else 0)


class ThingTypes:
    FIRST = 131
    AXE = 131
    SWORD = 132
    SPEAR = 133
    HELMET = 134
    COAT = 135
    BOOTS = 136
    KEY = 137
    MAP = 138
    BOMB = 139
    OAR = 140
    BOAT = 141
    LAST = 141


class Player:
    def __init__(self):
        self.strength = 100
        self.inventory = []
        self.gold = 0

    def __str__(self):
        return 'Ваша сила: {:.2f}<br/>Ваше золото: {}<br/>'.format(self.strength, self.gold) + \
            'У вас ничего нет!' if not self.inventory else \
            'У вас есть: <ul><li>' + '</li><li>'.join(self.inventory) + '</li></ul>'


def make_global_map():
    m = []
    SIZE = 20
    for i in range(SIZE):
        m.append([cell_factory(i, j, random.randint(10, 200)) for j in range(SIZE)])

    for i in range(SIZE):
        m[i][SIZE//2] = WaterCell(i, SIZE//2, random.randint(180, 181))
    return m


player = Player()
global_map = make_global_map()


@route('/')
def index():
    return 'Добро пожаловать в матрицу! <a href="/at/0/0">Вход здесь</a>, выхода нет.'


@route('/at/<x>/<y>')
def index(x, y):
    global global_map

    x = int(x)
    y = int(y)
    cell = global_map[x][y]

    page = (cell.on_enter(player) or 'Вот вы и здесь.') + '<hr/>'

    if player.strength <= 0:
        return page + '<hr/>Вы умерли!..'

    page += "{}<hr/> Вы находитесь в точке ({}, {}).<br/>Здесь: {}.<hr/>".format(player, x, y, cell)

    for action in cell.actions(player):
        page += '<a href="/at/{}/{}/{}">{}</a><br/>'.format(x, y, action['id'], action['name'])

    if x > 0:
        if global_map[x-1][y].is_passable(player):
            page += '<br/><a href="/at/{}/{}">Идти на север</a>'.format(x-1, y)
        else:
            page += '<br/>На севере {}'.format(global_map[x-1][y])
    if x < len(global_map)-1:
        if global_map[x+1][y].is_passable(player):
            page += '<br/><a href="/at/{}/{}">Идти на юг</a>'.format(x+1, y)
        else:
            page += '<br/>На юге {}'.format(global_map[x+1][y])
    if y > 0 and global_map[x][y-1].is_passable(player):
        if global_map[x][y-1].is_passable(player):
            page += '<br/><a href="/at/{}/{}">Идти на запад</a>'.format(x, y-1)
        else:
            page += '<br/>На западе {}'.format(global_map[x][y-1])
    if y < len(global_map[x])-1:
        if global_map[x][y+1].is_passable(player):
            page += '<br/><a href="/at/{}/{}">Идти на восток</a>'.format(x, y+1)
        else:
            page += '<br/>На востоке {}'.format(global_map[x][y+1])

    return page

run(host='localhost', port=8090)