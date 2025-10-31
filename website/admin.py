# Fichier : website/admin.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user 
from . import db 
from .decorateur import admin_required # Importe ton nouveau décorateur
from .models import Missions, User

admin = Blueprint('admin', __name__)

# La route est maintenant statique et protégée par le décorateur
@admin.route('/')
@admin_required
def admin_page():
    total_user = User.query.count()
    total_admin = User.query.filter_by(admin=True).count()
    users = User.query.all()


    return render_template('/admin/admin.html', total_users=total_user, total_admin=total_admin, users=users)


@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    # Retrieve the user by ID or return a 404 error if not found.
    user_to_delete = User.query.get_or_404(user_id)

    if user_to_delete.id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte.", category='danger')
        return redirect(url_for('admin.admin'))


    Missions.query.filter_by(user_id=user_to_delete.id).delete()

    # Delete the user from the database.
    db.session.delete(user_to_delete)
    db.session.commit()

    flash("Utilisateur supprimé avec succès.", category='success')
    return redirect(url_for('admin.dashboard'))