import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import get_db_connection  # Import our shared DB connection

# Create the blueprint (this acts like a mini-app for Student 1)
web_bp = Blueprint('web', __name__, template_folder='templates')

@web_bp.route('/')
def home():
    # If already logged in, skip the login page
    if 'role' in session:
        if session['role'] == 'Customer':
            return redirect(url_for('web.customer_dashboard'))
        elif session['role'] == 'Worker':
            return redirect(url_for('web.worker_dashboard'))
            
    return render_template('login.html')

@web_bp.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    phone = request.form['phone']
    password = request.form['password']
    role = request.form['role']
    
    hashed_password = generate_password_hash(password)

    cnic_filename = None
    is_verified = True # Customers are verified automatically

    if role == 'Worker':
        is_verified = False # Workers need manual admin approval
        cnic_file = request.files.get('cnic_image')
        if cnic_file and cnic_file.filename != '':
            cnic_filename = secure_filename(cnic_file.filename)
            cnic_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], cnic_filename))

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            'INSERT INTO "USER" (name, phone, password, role, cnic_image, is_verified) VALUES (%s, %s, %s, %s, %s, %s)',
            (name, phone, hashed_password, role, cnic_filename, is_verified)
        )
        conn.commit()
        flash('Account created successfully! Please log in.')
    except Exception as e:
        conn.rollback()
        flash(f'Error creating account. Phone number might already exist.')
    finally:
        cur.close()
        conn.close()
        
    # CRITICAL: Always return a response!
    return redirect(url_for('web.home'))


@web_bp.route('/login', methods=['POST'])
def login():
    phone = request.form['phone']
    password = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('SELECT name, password, role, is_verified FROM "USER" WHERE phone = %s', (phone,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and check_password_hash(user[1], password):
        session['user_name'] = user[0]
        session['role'] = user[2]
        session['is_verified'] = user[3]

        if session['role'] == 'Customer':
            return redirect(url_for('web.customer_dashboard'))
        elif session['role'] == 'Worker':
            return redirect(url_for('web.worker_dashboard'))
    else:
        flash('Invalid phone number or password. Please try again.')
    
    # CRITICAL: This acts as the safety net. If login fails, send them back to the home page!
    return redirect(url_for('web.home'))


@web_bp.route('/customer_dashboard')
def customer_dashboard():
    if session.get('role') == 'Customer':
        return render_template('customer_dashboard.html', user_name=session.get('user_name'))
    return redirect(url_for('web.home'))


@web_bp.route('/worker_dashboard')
def worker_dashboard():
    if session.get('role') == 'Worker':
        return render_template('worker_dashboard.html', 
                               user_name=session.get('user_name'), 
                               is_verified=session.get('is_verified'))
    return redirect(url_for('web.home'))


@web_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.')
    return redirect(url_for('web.home'))