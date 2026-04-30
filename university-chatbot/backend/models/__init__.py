from ..database import db
from datetime import datetime

class FAQ(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    intent = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<FAQ {self.question}>'

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChatLog {self.id}>'
