__author__ = 'Romanzi (Roman Sytnik)'

from bottle import get, post, run, request
import inflation_map

@get('/upload')
def upload_form():
    return '''
<form action="/upload" method="post" enctype="multipart/form-data">
  <input type="file" name="image" /><br />
  <input type="submit" />
</form>
    '''

@post('/upload')
def upload_submit():
    file_csv = request.get("image")
    map = inflation_map.InflationMap(file_csv)
    map.draw_image()
    return file_csv

run(host='localhost', port=8080, debug=True)