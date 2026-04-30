import unittest
import sys
import os

# Add project root to path so `backend` package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app, db, init_db
from backend.chatbot import get_response
from backend.models import FAQ, ChatLog


class TestChatbotLogic(unittest.TestCase):
    """Unit tests for the keyword-matching chatbot logic."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        # Seed one FAQ for deterministic tests
        faq = FAQ(
            question="How do I register for courses?",
            answer="Log in to the student portal and select Course Registration.",
            intent="registration"
        )
        db.session.add(faq)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    # --- Response logic tests ---

    def test_registration_query_returns_answer(self):
        response = get_response("How do I register?")
        self.assertTrue(len(response) > 0)
        self.assertNotIn("I'm sorry", response)

    def test_registration_keyword_match(self):
        response = get_response("register courses")
        self.assertIn("portal", response.lower())

    def test_fallback_for_unknown_input(self):
        response = get_response("xkqzwvmjlp")
        self.assertIn("I'm sorry", response)

    def test_greeting_hello(self):
        response = get_response("hello")
        self.assertIn("University", response)

    def test_greeting_hi(self):
        response = get_response("hi there")
        self.assertIn("University", response)

    def test_greeting_hey(self):
        response = get_response("hey")
        self.assertIn("University", response)

    def test_goodbye(self):
        response = get_response("bye")
        self.assertIn("Goodbye", response)

    def test_name_query(self):
        response = get_response("what is your name")
        self.assertIn("Chatbot", response)

    def test_empty_message_returns_fallback(self):
        response = get_response("")
        # Empty input should not crash; returns fallback or greeting
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_punctuation_stripped(self):
        # Punctuation-heavy query should still match
        response = get_response("register???")
        self.assertTrue(len(response) > 0)

    def test_case_insensitive_matching(self):
        resp_lower = get_response("register")
        resp_upper = get_response("REGISTER")
        self.assertEqual(resp_lower, resp_upper)

    # --- API endpoint tests ---

    def test_api_ask_endpoint_post(self):
        resp = self.client.post('/ask', data={'message': 'register'})
        self.assertEqual(resp.status_code, 200)

    def test_api_ask_returns_json(self):
        resp = self.client.post('/ask', data={'message': 'register'})
        data = resp.get_json()
        self.assertIn('response', data)

    def test_api_ask_response_not_empty(self):
        resp = self.client.post('/ask', data={'message': 'register'})
        data = resp.get_json()
        self.assertTrue(len(data['response']) > 0)

    def test_api_ask_no_message(self):
        resp = self.client.post('/ask', data={})
        data = resp.get_json()
        self.assertEqual(data['response'], 'Please enter a message.')

    def test_index_route_returns_html(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'UniAssistant', resp.data)

    def test_chat_log_saved(self):
        self.client.post('/ask', data={'message': 'register'})
        logs = ChatLog.query.all()
        self.assertGreater(len(logs), 0)

    def test_chat_log_stores_user_message(self):
        self.client.post('/ask', data={'message': 'register'})
        log = ChatLog.query.first()
        self.assertEqual(log.user_message, 'register')

    def test_chat_log_stores_bot_response(self):
        self.client.post('/ask', data={'message': 'register'})
        log = ChatLog.query.first()
        self.assertTrue(len(log.bot_response) > 0)

    # --- Database model tests ---

    def test_faq_model_created(self):
        count = FAQ.query.count()
        self.assertEqual(count, 1)

    def test_faq_repr(self):
        faq = FAQ.query.first()
        self.assertIn('FAQ', repr(faq))

    def test_chatlog_repr(self):
        log = ChatLog(user_message="hi", bot_response="Hello!")
        db.session.add(log)
        db.session.commit()
        self.assertIn('ChatLog', repr(log))


class TestChatbotWithMultipleFAQs(unittest.TestCase):
    """Tests with a richer FAQ dataset."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        db.create_all()
        faqs = [
            FAQ(question="Where is the library located?",
                answer="The library is in Building B, 2nd floor.", intent="campus"),
            FAQ(question="What are the library opening hours?",
                answer="Library hours: Mon-Fri 8am-10pm, Weekends 10am-6pm.", intent="campus"),
            FAQ(question="How do I apply for a scholarship?",
                answer="Apply via the Financial Aid page on the university website.", intent="finance"),
            FAQ(question="Where can I get a student ID card?",
                answer="Student ID cards are issued at the Student Affairs office.", intent="admin"),
            FAQ(question="Is there a health center on campus?",
                answer="Yes, the health center is in Building A, ground floor.", intent="campus"),
        ]
        db.session.bulk_save_objects(faqs)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_library_location_query(self):
        response = get_response("Where is the library?")
        self.assertIn("Building B", response)

    def test_library_hours_query(self):
        response = get_response("library hours")
        self.assertIn("8am", response)

    def test_scholarship_query(self):
        response = get_response("scholarship application")
        self.assertIn("Financial Aid", response)

    def test_student_id_query(self):
        response = get_response("student ID card")
        self.assertIn("Student Affairs", response)

    def test_health_center_query(self):
        response = get_response("health center campus")
        self.assertIn("Building A", response)

    def test_threshold_not_triggered_on_weak_match(self):
        # Single vague word unlikely to score >= 0.3 against all questions
        response = get_response("building")
        # Either matches something or returns fallback — no crash
        self.assertIsInstance(response, str)

    def test_multiple_faq_best_match(self):
        # "library location" should match the location FAQ, not hours
        response = get_response("library location building")
        self.assertIn("Building B", response)


if __name__ == '__main__':
    unittest.main(verbosity=2)
