"""app.py: render and route to webpages"""

import os
import re
import logging
import bcrypt
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from db.query import get_all, get_session, get_user_by_email
from db.server import init_database
from db.schema import Users

# load environment variables from .env
load_dotenv()

# Setup logging
logs_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

logging.basicConfig(
    filename=os.path.join(logs_dir, 'app.log'),
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('app')

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app
    app = Flask(__name__,
                template_folder=os.path.join(os.getcwd(), 'templates'),
                static_folder=os.path.join(os.getcwd(), 'static'))

    # Set secret key for flash messages
    app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # connect to db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    # Initialize database
    with app.app_context():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            exit(1)

    session = get_session()

    # ===============================================================
    # routes
    # ===============================================================

    # create a webpage based off of the html in templates/index.html
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET','POST'])
    def signup():
        """Sign up page: enables users to sign up"""
        if request.method == 'POST':
            fname = request.form["firstname"].strip()
            lname = request.form["lastname"].strip()
            email = request.form["email"].strip()
            phnum = request.form["phone"].strip()
            pword = request.form["password"].strip()

            # Check for potentially malicious input
            malicious_patterns = [
                r'.*(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b).*',  # SQL keywords
                r'.*[<>\"\';].*',  # HTML/script tags, quotes, semicolons
                r'.*(javascript:|data:|vbscript:).*',  # Script protocols
            ]

            def is_malicious_input(text):
                if len(text) > 100:  # Suspiciously long input
                    return True
                for pattern in malicious_patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        return True
                return False

            if is_malicious_input(fname) or is_malicious_input(lname) or is_malicious_input(email):
                logger.warning(f'Malicious input detected - fname: {fname}, lname: {lname}, email: {email}')
                flash('Invalid input detected.')

            is_valid = True

            if not re.match(r'^[a-zA-Z]+$', fname):
                flash('First name must contain only letters.')
                is_valid = False

            if not re.match(r'^[a-zA-Z]+$', lname):
                flash('Last name must contain only letters.')
                is_valid = False

            if not re.match(r'^[0-9]{10}$', phnum):
                flash('Phone number must be exactly 10 digits.')
                is_valid = False

            if not email:
                flash('Email is required.')
                is_valid = False

            if is_valid:
                try:
                    hashed_password = bcrypt.hashpw(pword.encode('utf-8'), bcrypt.gensalt())

                    user = Users(
                            FirstName=fname,
                            LastName=lname,
                            Email=email,
                            PhoneNumber=phnum,
                            Password=hashed_password.decode('utf-8')
                            )

                    session.add(user)
                    session.commit()

                    return redirect(url_for("success"))
                except Exception as e:
                    session.rollback()
                    print("error inserting user record:", e)
                    flash('An error occurred while creating your account. Please try again.')
                finally:
                    session.close()

        return render_template('signup.html')
    
    @app.route('/login', methods=['GET','POST'])
    def login():
        """Log in page: enables users to log in"""
        if request.method == 'POST':
            email = request.form["email"].strip()
            password = request.form["password"].strip()

            user = get_user_by_email(email)

            if not user:
                logger.warning(f'Failed login attempt: user not found - email: {email}')
                flash('No account found with this email address.')
            elif not bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):
                logger.warning(f'Failed login attempt: wrong password - email: {email}')
                flash('Incorrect password.')
            else:
                return redirect(url_for("success"))

        return render_template('login.html')

    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = get_all(Users)
        
        return render_template('users.html', users=all_users)

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        return render_template('success.html')

    @app.errorhandler(404)
    def page_not_found(e):
        """Log routing failures (404 errors)"""
        logger.warning(f'404 error - Path: {request.path}, Method: {request.method}, IP: {request.remote_addr}')
        return render_template('404.html'), 404

    return app

if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)
