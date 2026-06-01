# Fix-it: Home Services & Blind Bidding Platform

This repository contains the source code for the Fix-it application (Assignment-04), designed by Muhammad Huzaifa Saqib and Ashir Ali. 

The architecture is divided into two main domains using Flask Blueprints:
1. **Web Module:** A desktop portal for user authentication and dashboard management.
2. **Mobile Module:** A mobile-responsive web app featuring a Blind Bidding Engine.

## Tech Stack
* **Backend:** Python (Flask)
* **Database:** PostgreSQL (Hosted on Supabase)
* **Frontend:** HTML, CSS, Jinja2 Templates

## How to Run Locally
1. Clone this repository.
2. Create a virtual environment and install dependencies: `pip install flask psycopg2-binary werkzeug`
3. Update `database.py` with your Supabase credentials.
4. Run the server: `python app.py`
5. Access the app at `http://127.0.0.1:5000`
