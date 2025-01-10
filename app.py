from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2.types import Geography, Geometry
from geoalchemy2.shape import from_shape
from shapely.geometry import Point, MultiPolygon
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

print('Connessione avvenuta con successo!')

@app.route('/')
def dajeromadaje():
    return 'dajeroma'

@app.route('/add_edificio', methods=['GET', 'POST'])
def add_edificio():
    try:
        data = request.get_json()

        codice_istat = data.get('codice_istat')
        posizione = data.get('posizione')
        perimetro = data.get('perimetro')

        if not codice_istat or not posizione:
            return jsonify({'error': 'codice_istat e posizione sono obbligatori'}), 400

        posizione_point = from_shape(Point(posizione[0], posizione[1]), srid=4326)

        perimetro_geom = None
        if perimetro:
            polygons = [MultiPolygon([[(x, y) for x, y in ring]]) for ring in perimetro]
            perimetro_geom = from_shape(MultiPolygon(polygons), srid=4326)

        nuovo_edificio = Edificio(
            codice_istat=codice_istat,
            posizione=posizione_point,
            perimetro=perimetro_geom
        )

        db.session.add(nuovo_edificio)
        db.session.commit()

        return jsonify({'message': 'Edificio aggiunto con successo!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)