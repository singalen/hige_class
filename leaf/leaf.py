__author__ = 'Romanzi (Roman Sytnik)'

from folium import Map
map_osm = Map(location=[32.5236, 48.6750])
map_osm.create_map(path='osm.html')