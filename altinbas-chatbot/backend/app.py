from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import requests
import sqlite3
import json
import uuid
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
DATABASE_PATH = "university_chatbot.db"

# =============================================================================
# DATABASE MANAGER CLASS
# =============================================================================

class DatabaseManager:
    """Handles all database operations for the chatbot"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # FAQs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category VARCHAR(50),
                question TEXT,
                answer TEXT,
                intent_name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User queries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id VARCHAR(100),
                query TEXT,
                intent_detected VARCHAR(100),
                confidence_score FLOAT,
                response TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER,
                rating INTEGER,
                comment TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (query_id) REFERENCES user_queries(id)
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                total_queries INTEGER DEFAULT 0,
                successful_queries INTEGER DEFAULT 0,
                failed_queries INTEGER DEFAULT 0,
                avg_confidence FLOAT,
                unique_users INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    
    def log_query(self, user_id, query, intent, confidence, response):
        """Log user query to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_queries 
                (user_id, query, intent_detected, confidence_score, response)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, query, intent, confidence, response))
            conn.commit()
            query_id = cursor.lastrowid
            conn.close()
            return query_id
        except Exception as e:
            print(f"❌ Error logging query: {e}")
            return None
    
    def save_feedback(self, query_id, rating, comment):
        """Save user feedback"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO feedback (query_id, rating, comment)
                VALUES (?, ?, ?)
            ''', (query_id, rating, comment))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error saving feedback: {e}")
            return False
    
    def get_analytics(self, days=7):
        """Get analytics for the last N days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total queries
            cursor.execute('''
                SELECT COUNT(*) FROM user_queries 
                WHERE DATE(timestamp) >= DATE('now', '-' || ? || ' days')
            ''', (days,))
            total_queries = cursor.fetchone()[0]
            
            # Average confidence
            cursor.execute('''
                SELECT AVG(confidence_score) FROM user_queries 
                WHERE DATE(timestamp) >= DATE('now', '-' || ? || ' days')
            ''', (days,))
            avg_confidence = cursor.fetchone()[0] or 0
            
            # Unique users
            cursor.execute('''
                SELECT COUNT(DISTINCT user_id) FROM user_queries 
                WHERE DATE(timestamp) >= DATE('now', '-' || ? || ' days')
            ''', (days,))
            unique_users = cursor.fetchone()[0]
            
            # Top intents
            cursor.execute('''
                SELECT intent_detected, COUNT(*) as count 
                FROM user_queries 
                WHERE DATE(timestamp) >= DATE('now', '-' || ? || ' days')
                GROUP BY intent_detected 
                ORDER BY count DESC 
                LIMIT 5
            ''', (days,))
            top_intents = cursor.fetchall()
            
            # Average rating
            cursor.execute('''
                SELECT AVG(rating) FROM feedback 
                WHERE DATE(timestamp) >= DATE('now', '-' || ? || ' days')
            ''', (days,))
            avg_rating = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'total_queries': total_queries,
                'avg_confidence': round(avg_confidence, 2),
                'unique_users': unique_users,
                'top_intents': [{'intent': i[0], 'count': i[1]} for i in top_intents],
                'avg_rating': round(avg_rating, 2)
            }
        except Exception as e:
            print(f"❌ Error getting analytics: {e}")
            return None

# Initialize database manager
db = DatabaseManager()

# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def home():
    """Serve the main chatbot interface"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Altinbas University FAQ Chatbot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .chat-container {
                width: 100%;
                max-width: 600px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                overflow: hidden;
                display: flex;
                flex-direction: column;
                height: 600px;
            }
            .chat-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }
            .chat-header h2 {
                margin-bottom: 5px;
            }
            .chat-header p {
                font-size: 14px;
                opacity: 0.9;
            }
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f5f5f5;
            }
            .message {
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 10px;
                max-width: 80%;
                animation: fadeIn 0.3s;
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .bot-message {
                background: white;
                margin-right: auto;
                border: 1px solid #e0e0e0;
            }
            .user-message {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: auto;
            }
            .typing-indicator {
                display: inline-block;
            }
            .typing-indicator span {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #667eea;
                margin: 0 2px;
                animation: typing 1.4s infinite;
            }
            .typing-indicator span:nth-child(2) {
                animation-delay: 0.2s;
            }
            .typing-indicator span:nth-child(3) {
                animation-delay: 0.4s;
            }
            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-10px); }
            }
            .chat-input {
                display: flex;
                padding: 20px;
                background: white;
                border-top: 1px solid #e0e0e0;
            }
            .chat-input input {
                flex: 1;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 14px;
                outline: none;
            }
            .chat-input input:focus {
                border-color: #667eea;
            }
            .chat-input button {
                margin-left: 10px;
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-weight: bold;
                transition: transform 0.2s;
            }
            .chat-input button:hover {
                transform: scale(1.05);
            }
            .chat-input button:active {
                transform: scale(0.95);
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h2>🎓 Altinbas University Assistant</h2>
                <p>Ask me anything about university services!</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">
                    <p>Hello! I'm your Altinbas University assistant. I can help you with information about registration, courses, campus facilities, and more. What would you like to know?</p>
                </div>
            </div>
            
            <div class="chat-input">
                <input type="text" id="userInput" placeholder="Type your question here..." />
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <script>
            let userId = null;

            function sendMessage() {
                const input = document.getElementById('userInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                showTypingIndicator();
                
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        user_id: userId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    removeTypingIndicator();
                    userId = data.user_id;
                    addMessage(data.response, 'bot');
                })
                .catch(error => {
                    removeTypingIndicator();
                    addMessage('Sorry, something went wrong. Please try again.', 'bot');
                    console.error('Error:', error);
                });
            }

            function addMessage(text, sender) {
                const messagesDiv = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.innerHTML = `<p>${text}</p>`;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            function showTypingIndicator() {
                const messagesDiv = document.getElementById('chatMessages');
                const typingDiv = document.createElement('div');
                typingDiv.className = 'message bot-message typing-indicator';
                typingDiv.id = 'typingIndicator';
                typingDiv.innerHTML = '<span></span><span></span><span></span>';
                messagesDiv.appendChild(typingDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            function removeTypingIndicator() {
                const indicator = document.getElementById('typingIndicator');
                if (indicator) indicator.remove();
            }

            document.getElementById('userInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and communicate with Rasa"""
    try:
        data = request.json
        user_message = data.get('message')
        user_id = data.get('user_id') or str(uuid.uuid4())
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Send message to Rasa
        rasa_response = requests.post(
            RASA_API_URL,
            json={"sender": user_id, "message": user_message},
            timeout=10
        )
        
        if rasa_response.status_code == 200:
            bot_responses = rasa_response.json()
            
            if bot_responses:
                # Join all text responses from Rasa
                bot_message = "\n".join([r.get('text', '') for r in bot_responses if 'text' in r])
                if not bot_message:
                    bot_message = "I'm sorry, I received an empty response."
                
                # Extract intent and confidence if available (optional enhancement)
                intent = 'unknown'
                confidence = 0.0
                
                # Log the interaction
                query_id = db.log_query(
                    user_id=user_id,
                    query=user_message,
                    intent=intent,
                    confidence=confidence,
                    response=bot_message
                )
                
                return jsonify({
                    'response': bot_message,
                    'user_id': user_id,
                    'query_id': query_id
                })
            else:
                return jsonify({
                    'response': 'I apologize, I am having trouble responding right now. Please try again.',
                    'user_id': user_id
                })
        else:
            return jsonify({
                'response': 'Sorry, I am currently unavailable. Please try again later.',
                'user_id': user_id
            }), 500
            
    except requests.exceptions.Timeout:
        return jsonify({
            'response': 'Request timed out. Please try again.',
            'user_id': user_id
        }), 504
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Handle user feedback submission"""
    try:
        data = request.json
        query_id = data.get('query_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not query_id or not rating:
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = db.save_feedback(query_id, rating, comment)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Thank you for your feedback!'
            })
        else:
            return jsonify({'error': 'Failed to save feedback'}), 500
            
    except Exception as e:
        print(f"❌ Error in feedback endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get chatbot usage analytics"""
    try:
        days = request.args.get('days', 7, type=int)
        analytics = db.get_analytics(days)
        
        if analytics:
            return jsonify(analytics)
        else:
            return jsonify({'error': 'Failed to retrieve analytics'}), 500
            
    except Exception as e:
        print(f"❌ Error in analytics endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check Rasa connection
        rasa_health = requests.get('http://localhost:5005/', timeout=5)
        rasa_status = 'online' if rasa_health.status_code == 200 else 'offline'
    except:
        rasa_status = 'offline'
    
    return jsonify({
        'status': 'online',
        'rasa': rasa_status,
        'timestamp': datetime.now().isoformat()
    })

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Starting Altinbas University Chatbot Backend")
    print("=" * 60)
    print("📊 Initializing database...")
    print("🌐 Starting Flask server on http://localhost:5000")
    print("🤖 Make sure Rasa is running on http://localhost:5005")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
