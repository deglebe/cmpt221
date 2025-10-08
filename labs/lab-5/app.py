"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template
from db.server import init_database, get_session

# load environment variables from .env
load_dotenv()

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
    
    # connect to db
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    
    # Initialize database
    # with app.app_context():
    #     if not init_database():
    #         print("Failed to initialize database. Exiting.")
            # exit(1)

    # ===============================================================
    # routes
    # ===============================================================

    # captcha page
    @app.route('/')
    def captcha():
        """Captcha page"""
        return render_template('captcha.html')
    
    # main page after captcha completion
    @app.route('/index')
    def index():
        """Home page"""
        return render_template('index.html')

    # cats page
    @app.route('/cats')
    def cats():
        """Cats page"""
        return render_template('cats.html')

    # warning page
    @app.route('/warning')
    def warning():
        """Warning page"""
        return render_template('warning.html')

    return app

if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)
