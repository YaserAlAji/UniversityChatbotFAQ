from flask import Flask, render_template, request, jsonify
from .database import db
from .models import ChatLog, FAQ
from .chatbot import get_response
import os

# Initialize Flask with specific template and static folders
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Configure database
db_path = os.path.join(os.path.dirname(__file__), '../data/chatbot.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'university_secret_key'

db.init_app(app)

# .. imports ..

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('message')
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})

    bot_response = get_response(user_message)

    # Log the interaction
    try:
        log = ChatLog(user_message=user_message, bot_response=bot_response)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging chat: {e}")

    return jsonify({'response': bot_response})

def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    # Ensure data directory exists
    data_dir = os.path.dirname(db_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Initialize DB if not exists
    if not os.path.exists(db_path):
        init_db()
    
    app.run(debug=True)
