from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os # We'll use this for deployment configuration later

# --- APPLICATION SETUP ---
app = Flask(__name__)

# Configure the SQLite database
# The OS environ check is good practice for deployment vs. local
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///site.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODEL (Guestbook Table) ---
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        # This is what prints when you look at the object in the shell
        return f'<Guest {self.name}>'

# --- ROUTES ---

@app.route("/", methods=['GET', 'POST'])
def home():
    # Handle the form submission (POST request)
    if request.method == 'POST':
        # Safely retrieve the name from the submitted form data
        guest_name = request.form.get('name_input')
        
        if guest_name:
            # Create a new Guest object and save it to the database
            new_guest = Guest(name=guest_name.title())
            db.session.add(new_guest)
            db.session.commit()
            
            # Redirect to the GET route to prevent form resubmission on refresh
            return redirect(url_for('home'))

    # Handle the page display (GET request)
    # Fetch all guests from the database for display
    guests = Guest.query.all()
    
    # Render the template, passing the list of guests
    return render_template("index.html", guests=guests)

# --- DATABASE INITIALIZATION AND RUN BLOCK ---

# Function to create the database tables if they don't exist
def init_db():
    # Use the application context to safely interact with Flask extensions
    with app.app_context():
        # This creates the site.db file and the Guest table
        db.create_all()

# This block only runs when you execute 'python3 app.py' directly
if __name__ == "__main__":
    init_db()  # <-- Initializes the DB file/tables on first run
    app.run(debug=True)