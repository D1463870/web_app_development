import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    # Load environment variables
    load_dotenv()
    
    # Initialize Flask app
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_secret')
    
    # Import and register routing blueprints
    from app.routes.auth import auth_bp
    from app.routes.records import records_bp
    from app.routes.categories import categories_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(dashboard_bp)
    
    return app

app = create_app()

def init_db():
    """Initializes the database using schema.sql"""
    import sqlite3
    os.makedirs('instance', exist_ok=True) # Usually sqlite db is placed in instance or root
    conn = sqlite3.connect('app.db')
    try:
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
