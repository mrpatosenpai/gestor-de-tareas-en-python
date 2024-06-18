from flask import Flask
from app.app import db
import datetime

class Tareas(db.Model):
    id_t = db.Colum(db.Interger, Primary_Key = True)
    nombre = db.Colum(db.String(200), nullable = False)
    fechainicio = db.Colum(db.DateTime, default=datetime.utcnow)
    fechafin = db.Colum(db.DataTime)
    estado= db.Colum(db.String(20), default= 'Por asignar')