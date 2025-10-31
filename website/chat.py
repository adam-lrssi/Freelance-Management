# Fichier : website/chat.py

from flask_login import login_required, current_user
from flask_socketio import emit, join_room, leave_room
from . import socketio
from flask import Blueprint, render_template, request, flash

chat = Blueprint('chat', __name__)

# Liste des utilisateurs en ligne
online_users = {}

@chat.route('/')
@login_required
def chat_page():
    return render_template('chat/chat_page.html')

@socketio.on('connect')
def handle_connect():
    # 💡 Associez la session de SocketIO à l'utilisateur
    if current_user.is_authenticated:
        online_users[request.sid] = current_user.name
        print(f'{current_user.name} est connecté.')
        
        # Mettez à jour la liste des utilisateurs pour tous les clients
        emit('update_users', {'user_list': list(online_users.values())}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in online_users:
        username = online_users[request.sid]
        del online_users[request.sid]
        print(f'{username} est déconnecté.')
        
        # Mettez à jour la liste des utilisateurs pour tous les clients
        emit('update_users', {'user_list': list(online_users.values())}, broadcast=True)

@socketio.on('message')
def handle_message(data):
    message = data.get('message')
    if message:
        username = online_users.get(request.sid, 'Anonyme')
        print(f"Message reçu de {username}: {message}")
        emit('new_message', {'user': username, 'message': message}, broadcast=True)