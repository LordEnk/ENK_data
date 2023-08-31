#!/usr/bin/env python3
'''guest user authentication'''

from models import User, Guest

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        guest = Guest.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Regular user login process
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('auth.profile'))
        elif guest:
            # Guest user login without a password
            login_user(guest)
            flash('Guest login successful', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Login unsuccessful. Please try again with the correct credentials.', 'danger')
    return render_template('login.html')
