# -*- coding: utf-8 -*-
__author__ = 'Romanzi (Roman Sytnik)'

# у меня возникли проблемы с импортом на интерпритаторе 3.3., когда я подключил 2.7, то всё заработало

import mapnik

m = mapnik.Map(600, 300)
m.background = mapnik.Color('steelblue')

# создаём свой стиль
s = mapnik.Style()
r = mapnik.Rule() # rule object to hold symbolizers
# to fill a polygon we create a PolygonSymbolizer
polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9'))
r.symbols.append(polygon_symbolizer) # add the symbolizer to the rule object
# to add outlines to a polygon we create a LineSymbolizer
line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'), 0.1)
r.symbols.append(line_symbolizer) # add the symbolizer to the rule object
s.rules.append(r) # now add the rule to the style and we're done

m.append_style('My Style', s)
ds = mapnik.Shapefile(file='data/sample/ne_10m_admin_0_countries.shp')

layer = mapnik.Layer('world') # new layer called 'world' (we could name it anything)
layer.datasource = ds
layer.styles.append('My Style')

m.layers.append(layer)
m.zoom_all()

mapnik.render_to_file(m,'world.png', 'png')