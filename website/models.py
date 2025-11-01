# Fichier : website/models.py
import datetime
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

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    freelance_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())  # Changed this line
    
    # Relations
    messages = db.relationship('Message', backref='conversation', lazy=True)
    freelance = db.relationship('User', foreign_keys=[freelance_id])
    client = db.relationship('User', foreign_keys=[client_id])

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())
    is_read = db.Column(db.Boolean, default=False)
    # Add the conversation foreign key
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])