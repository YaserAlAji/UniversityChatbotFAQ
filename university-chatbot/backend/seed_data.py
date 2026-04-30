from app import app, db
from models import FAQ

def seed_faqs():
    faqs = [
        {
            "question": "How do I register for courses?",
            "answer": "To register for courses, log in to the student portal, go to the 'Academics' tab, and select 'Course Registration'. Follow the instructions to add courses to your schedule.",
            "intent": "registration"
        },
        {
            "question": "When is the deadline for registration?",
            "answer": "The deadline for course registration for the Fall semester is September 15th. For Spring, it is February 10th.",
            "intent": "registration"
        },
        {
            "question": "Where is the library located?",
            "answer": "The main library is located in Building B, on the 2nd floor. It is open directly from the main campus entrance.",
            "intent": "campus"
        },
        {
            "question": "What are the library opening hours?",
            "answer": "The library is open from 8:00 AM to 10:00 PM, Monday through Friday. On weekends, it is open from 10:00 AM to 6:00 PM.",
            "intent": "campus"
        },
        {
            "question": "How can I contact the computer engineering department?",
            "answer": "You can contact the Computer Engineering department via email at ce@university.edu or visit their office in Building C, Room 304.",
            "intent": "contact"
        },
        {
            "question": "What programs does the university offer?",
            "answer": "The university offers a wide range of undergraduate and graduate programs in Engineering, Business, Arts, and Sciences. Please visit the 'Academics' section on the website for a full list.",
            "intent": "programs"
        },
        {
            "question": "How do I check my exam schedule?",
            "answer": "Exam schedules are published on the student portal two weeks before the exam period. You can view them under 'My Exams'.",
            "intent": "exams"
        },
        {
            "question": "Where can I get a student ID card?",
            "answer": "You can obtain your student ID card at the Student Affairs office in the Administration Building. Please bring a valid photo ID.",
            "intent": "admin"
        },
        {
            "question": "Is there a health center on campus?",
            "answer": "Yes, the health center is located in Building A, ground floor. It provides basic medical services to students and staff.",
            "intent": "campus"
        },
        {
            "question": "How do I apply for a scholarship?",
            "answer": "Scholarship applications are available on the Financial Aid page of the university website. Deadlines vary by scholarship type.",
            "intent": "finance"
        }
    ]

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if data already exists to avoid duplicates
        if FAQ.query.count() > 0:
            print("Database already contains data. Skipping seed.")
            return

        for data in faqs:
            faq = FAQ(question=data['question'], answer=data['answer'], intent=data['intent'])
            db.session.add(faq)
        
        db.session.commit()
        print(f"Successfully added {len(faqs)} FAQs to the database.")

if __name__ == '__main__':
    seed_faqs()
