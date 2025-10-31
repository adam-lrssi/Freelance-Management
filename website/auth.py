from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_remembered, login_required, current_user, logout_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Veuillez vérifier vos informations de connexion.', category='danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)

        # 💡 Redirection basée sur le rôle de l'utilisateur
        if user.role == 'Client':
            return redirect(url_for('site.client_dashboard'))
        elif user.role == 'Freelance':
            return redirect(url_for('site.dashboard'))
        else:
            # Redirection par défaut pour les autres rôles (par exemple, admin)
            return redirect(url_for('site.dashboard'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash('L\'email est déjà lié à un compte.', category='danger')
        elif len(email) < 4:
            flash('L\'email doit être sous forme : xyz@exemple.com', category='danger')
        elif len(name) < 2:
            flash('Votre nom ne peut pas faire moins de 2 caractères.', category='danger')
        elif password1 != password2:
            flash('Les mots de passe ne correspondent pas.', category='danger')
        elif len(password1) < 7:
            flash('Votre mot de passe doit faire minimum 7 caractères.', category='danger')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'), role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Compte créé avec succès', category='success')
            
            # The 'dashboard' route is now a static route, not dynamic
            # It's better to redirect there without the username
            return redirect(url_for('site.dashboard'))

    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))