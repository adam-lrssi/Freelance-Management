# Fichier : website/models.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), nullable=False, default='Client')
    
    # Relations qui pointent vers les missions.
    # missions_assigned représente les missions que le freelance a créées
    missions_assigned = db.relationship('Missions', foreign_keys='Missions.freelance_id', backref='creator', lazy=True)
    # missions_created représente les missions qui ont été créées pour le client
    missions_created = db.relationship('Missions', foreign_keys='Missions.user_id', backref='client', lazy=True)


class Missions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False) 
    date_created = db.Column(db.DateTime, default=func.now()) 
    status = db.Column(db.String(50), default='En attente') 
    
    # Le client à qui la mission est assignée
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    # Le freelance qui a créé la mission
    freelance_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)