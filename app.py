import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, Response, flash
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thecodex'


@app.route('/geodata', methods=['GET', 'POST'])
def geodata():
    conn = sqlite3.connect('coords.sqlite3')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == 'GET':
        coords = []
        try:
            c.execute('SELECT * FROM PhotosCoordinates')
            fetched_coords = c.fetchall()
            db_coords = []
            for row in fetched_coords:
                coord = {
                    'id': row['id'],
                    'properties': {
                        'name': row['name']
                    },
                    'geometry': {
                        'coordinates': [row['lot'], row['lan']]
                    }
                }
                db_coords.append(coord)

            r = requests.get('http://localhost:8010/')
            json_coords = r.json()

            coords = json_coords['data']
            coords.extend(db_coords)
        except:
            flash('Database error')
            conn.rollback()
        finally:
            return render_template('home.html', coords=list(reversed(coords)), length=len(coords))

    if request.method == 'POST':
        try:
            name = request.form['name']
            lot = request.form['lot']
            lan = request.form['lan']
            c.execute('INSERT INTO PhotosCoordinates(name, lot, lan) VALUES (?, ?, ?)', (name, lot, lan))
            conn.commit()
            message = 'Record successfully added'
        except:
            conn.rollback()
            message = 'Database error'
        finally:
            return redirect(url_for('geodata'))


@app.route('/geodata/create')
def create_coords():
    form = forms.CoordsForm()
    return render_template('create_coords.html', form=form)


@app.route('/geodata/<int:coords_id>/edit')
def edit_coords(coords_id):
    conn = sqlite3.connect('coords.sqlite3')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    form = forms.CoordsForm()
    c.execute('SELECT * FROM PhotosCoordinates WHERE id=(?)', [str(coords_id)])
    coords = c.fetchone()
    form.id.data = coords['id']
    form.name.data = coords['name']
    form.lot.data = coords['lot']
    form.lan.data = coords['lan']
    return render_template('edit_coords.html', form=form)


@app.route('/geodata/<int:coords_id>', methods=['PUT', 'DELETE'])
def update_coords(coords_id):
    if request.method == 'PUT':
        conn = sqlite3.connect('coords.sqlite3')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        data = request.get_json()
        name = data['name']
        lot = data['lot']
        lan = data['lan']

        c.execute('UPDATE PhotosCoordinates SET name=(?), lot=(?), lan=(?) WHERE id=(?)', (name, lot, lan, coords_id))
        conn.commit()

        return Response(status=200)

    if request.method == 'DELETE':
        pass


if __name__ == '__main__':
    app.run(debug=True)
