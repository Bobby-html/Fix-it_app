from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db_connection

# Create the mobile blueprint
mobile_bp = Blueprint('mobile', __name__, template_folder='templates')

@mobile_bp.route('/mobile/feed')
def mobile_feed():
    if session.get('role') != 'Worker':
        return "Access Denied. Worker Portal Only."
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM GIG WHERE status = 'Posted'")
    gigs = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('mobile_feed.html', gigs=gigs, user_name=session.get('user_name'))

@mobile_bp.route('/submit_bid', methods=['POST'])
def submit_bid():
    gig_id = request.form['gig_id']
    price = request.form['price']
    time = request.form['time']
    worker_name = session.get('user_name') # Get the logged-in worker's name
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Insert the bid into the database
        cur.execute(
            'INSERT INTO BID (gigID, worker_name, price, estimatedTime) VALUES (%s, %s, %s, %s)',
            (gig_id, worker_name, price, time)
        )
        conn.commit()
        flash('Bid submitted successfully! The customer will review it.')
    except Exception as e:
        conn.rollback()
        print(f"Error submitting bid: {e}")
    finally:
        cur.close()
        conn.close()
        
    # CRITICAL: This return statement was missing! It sends the user back to the feed.
    return redirect(url_for('mobile.mobile_feed'))

@mobile_bp.route('/mobile/compare')
def mobile_compare():
    if session.get('role') != 'Customer':
        return "Access Denied. Customer Portal Only."
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM BID WHERE status = 'Pending'")
    bids = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('mobile_compare.html', bids=bids, user_name=session.get('user_name'))