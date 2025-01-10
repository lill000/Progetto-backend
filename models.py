from .app import db 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, DateTime
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography, Geometry

db = SQLAlchemy()

class Edificio(db.Model):
    __tablename__ = 'edificio'
    
    id = db.Column(db.Integer, primary_key=True)
    posizione = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=False)
    perimetro = db.Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)
    codice_istat = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return f"<Edificio {self.id} - {self.codice_istat}>"



class TerminazioneOttica(db.Model):
    __tablename__ = 'terminazione_ottica'
    
    id = db.Column(db.Integer, primary_key=True)
    id_edificio = db.Column(db.Integer, db.ForeignKey('edificio.id'), nullable=False)
    piano = db.Column(db.String(50), nullable=True)
    scala = db.Column(db.String(50), nullable=True)
    interno = db.Column(db.String(50), nullable=True)
    posizione_dettagliata = db.Column(db.Text, nullable=True)
    
    edificio = db.relationship('Edificio', backref=db.backref('terminazioni_ottiche', lazy=True))

    def __repr__(self):
        return f"<TerminazioneOttica {self.id} - {self.id_edificio}>"