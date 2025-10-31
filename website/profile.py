from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db 

profile = Blueprint('profile', __name__)

# The corrected profile_page function

@profile.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile_page(username):
    # Security check: make sure the logged-in user is viewing their own profile
    if current_user.name != username: 
        return render_template('error/404.html'), 403
    
    # Process the form submission
    if request.method == 'POST':
        new_email = request.form.get('email')
        new_name = request.form.get('name')
        
        # Update the current_user object directly
        current_user.email = new_email
        current_user.name = new_name
        
        # Commit the changes to the database
        db.session.commit()
        
        flash('Vos informations ont été mises à jour !', category='success')
        
        # Redirect the user to the new profile URL if the name changed
        return redirect(url_for('profile.profile_page', username=current_user.name))
    
    # Render the page for GET requests, passing the current_user object
    return render_template('user/profile.html', user=current_user)