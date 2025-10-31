# Fichier : website/site.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import Missions, User

site = Blueprint('site', __name__)

@site.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Client':
        return redirect(url_for('site.client_dashboard'))
    
    # 💡 Récupère toutes les missions créées par le freelance
    missions = Missions.query.filter_by(freelance_id=current_user.id).all()
    
    # 💡 Récupère tous les utilisateurs avec le rôle 'Client' pour la modale
    clients = User.query.filter_by(role='Client').all()
    missions = Missions.query.filter_by(freelance_id=current_user.id).all()


    return render_template('user/dashboard.html', user=current_user, missions=missions, clients=clients)

@site.route('/client-dashboard')
@login_required
def client_dashboard():
    # Ici, vous pourriez lister les missions du client.
    client_missions = Missions.query.filter_by(user_id=current_user.id).all()
    
    return render_template('user/client_dashboard.html', user=current_user, missions=client_missions)


@site.route('/add-mission', methods=['POST'])
@login_required
def add_mission():
    title = request.form.get('title')
    description = request.form.get('description')
    deadline_str = request.form.get('deadline')
    client_id = request.form.get('client_id')


    if not title or not deadline_str:
        flash('Le titre et la date limite sont obligatoires.', category='danger')
        return redirect(url_for('site.dashboard'))

    try:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
    except ValueError:
        flash('Format de date invalide.', category='danger')
        return redirect(url_for('site.dashboard'))

    new_missions = Missions(
        title=title,
        description=description,
        deadline=deadline,
        user_id=client_id, # Le client
        freelance_id=current_user.id # Le freelance
    )

    db.session.add(new_missions)
    db.session.commit()

    flash('Mission ajoutée avec succès !', category='success')
    return redirect(url_for('site.dashboard'))


@site.route('/dashboard/delete-mission/<int:mission_id>', methods=['POST'])
@login_required
def delete_mission(mission_id):
    # 💡 La ligne correcte pour récupérer la mission
    mission = Missions.query.get_or_404(mission_id)

    if mission.user_id != current_user.id:
        flash('Vous n\'êtes pas le créateur de cette mission.', category='danger')
        return redirect(url_for('site.dashboard'))

    db.session.delete(mission)
    
    # 💡 L'erreur est là : 'commit' est une méthode, il faut l'appeler avec des parenthèses
    db.session.commit()

    flash('Mission supprimée avec succès.', category='success')
    return redirect(url_for('site.dashboard'))

# Fichier : website/site.py

# ... vos imports


@site.route('/dashboard/edit_mission/<int:mission_id>', methods=['POST'])
@login_required
def edit_mission(mission_id):
    mission = Missions.query.get_or_404(mission_id)

    if mission.user_id != current_user.id:
        flash('Vous n\'êtes pas le créateur de cette mission.', category='danger')
        return redirect(url_for('site.dashboard'))
    
    # 💡 L'erreur est corrigée ici. On met à jour l'objet 'mission'.
    mission.title = request.form.get('title')
    mission.description = request.form.get('description')
    
    # Gère la conversion de la date
    new_deadline_str = request.form.get('deadline')
    if new_deadline_str:
        try:
            mission.deadline = datetime.strptime(new_deadline_str, '%Y-%m-%d')
        except ValueError:
            flash('Format de date invalide.', category='danger')
            return redirect(url_for('site.dashboard'))

    # Il n'est pas nécessaire d'ajouter l'objet à la session, il est déjà suivi.
    db.session.commit()

    flash('Mission modifiée avec succès.', category='success')
    return redirect(url_for('site.dashboard'))


@site.route('/update-mission-status/<int:mission_id>', methods=['POST'])
@login_required
def update_mission_status(mission_id):
    mission = Missions.query.get_or_404(mission_id)
    new_status = request.form.get('status')

    # 💡 Vérification de sécurité : Seul le freelance assigné peut mettre à jour le statut
    if mission.freelance_id != current_user.id:
        flash('Vous n\'êtes pas autorisé à modifier le statut de cette mission.', category='danger')
        return redirect(url_for('site.dashboard'))

    # Mettez à jour le statut et enregistrez dans la base de données
    mission.status = new_status
    db.session.commit()
    
    flash('Statut de la mission mis à jour !', category='success')
    return redirect(url_for('site.dashboard'))