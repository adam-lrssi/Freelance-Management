# Fichier : website/decorators.py

from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Vérifie si l'utilisateur est un admin
        if not current_user.is_authenticated or not current_user.admin:
            # Renvoie une erreur 403 Forbidden (Accès interdit)
            abort(403)
        return f(*args, **kwargs)
    return decorated_function