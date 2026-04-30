from .models import FAQ
from sqlalchemy import or_
import string

def get_response(user_message):
    """
    Process the user message and return a response from the database.
    Implements a simple keyword matching or fuzzy search.
    """
    # Clean user message: lower, strip, remove punctuation
    message = user_message.lower().strip()
    message = message.translate(str.maketrans('', '', string.punctuation))
    
    # Stopwords to ignore
    stopwords = {'what', 'are', 'the', 'is', 'how', 'do', 'i', 'to', 'can', 'in', 'of', 'does', 'where', 'when', 'a', 'an', 'help', 'me'}

    # Filter user words
    user_words = set(word for word in message.split() if word not in stopwords)
    
    # Query all FAQs
    faqs = FAQ.query.all()
    best_match = None
    max_overlap = 0 # Score 0 to 1
    
    for faq in faqs:
        # Clean question
        question_lower = faq.question.lower()
        question_lower = question_lower.translate(str.maketrans('', '', string.punctuation))
        
        question_words = set(word for word in question_lower.split() if word not in stopwords)
        
        if not question_words:
            continue

        # Calculate overlap
        intersection = user_words.intersection(question_words)
        match_count = len(intersection)
        
        # Score based on portion of question covered (Recall)
        # We prioritize questions that are "contained" in the user query or vice versa
        # Let's use Dice coefficient or simple Jaccard
        
        # Simple overlap ratio relative to question length (Recall)
        # If user asks "register", and question has "register", recall is 1.0 (if question only has "register")
        recall = match_count / len(question_words)
        
        if recall > max_overlap:
            max_overlap = recall
            best_match = faq
            
    # Threshold: at least 30% of key terms in question must be present in user query
    if best_match and max_overlap >= 0.3: 
        return best_match.answer

    # 2. Minimum Viable Fallback (Rule-based)
    if any(greet in message for greet in ["hello", "hi", "hey"]):
        return "Hello! I am the University Assistant. How can I help you today?"
    
    if "bye" in message:
        return "Goodbye! Have a great day."

    if "name" in message:
        return "I am the University AI Chatbot."

    # 3. Default response
    return "I'm sorry, I don't have information on that yet. Please contact the administration office."
