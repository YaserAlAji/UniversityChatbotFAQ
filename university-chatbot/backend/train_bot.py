import sys
import os

# Add the 'backend' folder to the python path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from app import app
from database import db
from models import FAQ

def train_bot():
    print("=== University Chatbot Training Mode ===")
    print("This tool allows you to add new Question & Answer pairs to the bot's knowledge base.")
    print("Type 'exit' or 'quit' at any time to stop.\n")

    with app.app_context():
        while True:
            question = input("Enter the new QUESTION: ").strip()
            if question.lower() in ['exit', 'quit']:
                break
            if not question:
                print("Question cannot be empty.")
                continue

            answer = input("Enter the ANSWER: ").strip()
            if answer.lower() in ['exit', 'quit']:
                break
            if not answer:
                print("Answer cannot be empty.")
                continue

            intent = input("Enter the category/intent (e.g., registration, library) [Optional]: ").strip()
            if intent.lower() in ['exit', 'quit']:
                break
            
            # Confirm
            print(f"\nReview:\nQ: {question}\nA: {answer}\nIntent: {intent}")
            confirm = input("Save this FAQ? (y/n): ").lower()
            
            if confirm == 'y':
                try:
                    new_faq = FAQ(question=question, answer=answer, intent=intent)
                    db.session.add(new_faq)
                    db.session.commit()
                    print("✅ Successfully added to database!\n")
                except Exception as e:
                    print(f"❌ Error saving to database: {e}\n")
            else:
                print("❌ Cancelled.\n")

    print("\nTraining session ended.")

if __name__ == '__main__':
    train_bot()
