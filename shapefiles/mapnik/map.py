# -*- coding: utf-8 -*-
import mapnik
__author__ = 'Romanzi (Roman Sytnik)'

# у меня возникли проблемы с импортом на интерпритаторе 3.3., когда я подключил 2.7, то всё заработало

stylesheet = 'world_population.xml'
image = 'world.png'
m = mapnik.Map(1200, 600)
mapnik.load_map(m, stylesheet)
m.zoom_all()

mapnik.render_to_file(m,'world.png', 'png')