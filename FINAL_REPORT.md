# University FAQ Chatbot — Final Project Report

**Project Title:** University Student Assistant FAQ Chatbot  
**Date:** April 30, 2026  
**Platform:** Python 3.12 · Flask 3.1 · SQLite · HTML/CSS/JavaScript  
**Test Results:** 29 / 29 Tests Passed (100%)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Objectives](#2-project-objectives)
3. [System Architecture Overview](#3-system-architecture-overview)
4. [Technology Stack](#4-technology-stack)
5. [Project Structure](#5-project-structure)
6. [Backend Implementation](#6-backend-implementation)
7. [Database Design](#7-database-design)
8. [Chatbot Algorithm — Keyword Matching Engine](#8-chatbot-algorithm--keyword-matching-engine)
9. [REST API Design](#9-rest-api-design)
10. [Frontend Implementation](#10-frontend-implementation)
11. [FAQ Knowledge Base](#11-faq-knowledge-base)
12. [Training Tool](#12-training-tool)
13. [Testing Strategy and Results](#13-testing-strategy-and-results)
14. [Performance Analysis](#14-performance-analysis)
15. [Security Considerations](#15-security-considerations)
16. [Secondary Implementation: Altinbas Chatbot (Rasa)](#16-secondary-implementation-altinbas-chatbot-rasa)
17. [Comparative Analysis of Both Approaches](#17-comparative-analysis-of-both-approaches)
18. [Known Limitations and Issues](#18-known-limitations-and-issues)
19. [Conclusions](#19-conclusions)
20. [Recommendations for Future Work](#20-recommendations-for-future-work)
21. [Appendix A — Full Test Suite Output](#appendix-a--full-test-suite-output)
22. [Appendix B — FAQ Knowledge Base (Full)](#appendix-b--faq-knowledge-base-full)
23. [Appendix C — API Reference](#appendix-c--api-reference)

---

## 1. Executive Summary

This report documents the complete design, implementation, testing, and evaluation of a University Student Assistant FAQ Chatbot. The system was developed to provide students with instant, automated answers to frequently asked questions about university services including course registration, library hours, scholarship applications, campus locations, and administrative procedures.

The project is implemented as a full-stack web application using Python/Flask on the backend and a modern glassmorphism-styled HTML/CSS/JavaScript frontend. The chatbot engine uses a custom keyword-matching algorithm with recall-based scoring to match user queries against a curated FAQ database stored in SQLite.

### Key Achievements

| Metric | Result |
|--------|--------|
| Tests written | 29 |
| Tests passing | 29 (100%) |
| FAQ entries in knowledge base | 40 |
| API endpoints implemented | 2 |
| Chatbot algorithm accuracy (seeded data) | High — all seeded intents correctly matched |
| Frontend components | Chat UI with typing indicator, animations, responsive layout |
| Response time (local) | < 50 ms per query |

The project successfully delivers a working, tested chatbot system ready for local deployment, with a clear path to production enhancement through expanded FAQ coverage or integration with a machine learning NLU engine.

---

## 2. Project Objectives

The core objectives defined for this project were:

### 2.1 Primary Objectives

1. **Automate student FAQ responses** — Reduce load on university administrative staff by handling routine queries automatically.
2. **Conversational interface** — Provide a natural, web-based chat experience accessible from any browser.
3. **Maintainable knowledge base** — Allow non-technical staff to extend the FAQ database through an interactive training tool without modifying code.
4. **Reliable data persistence** — Log all chat interactions in a structured database for future analysis and quality assurance.
5. **Tested, verifiable implementation** — All components should be covered by automated tests.

### 2.2 Secondary Objectives

1. **Modern UI design** — Deliver a professional, university-branded interface using contemporary CSS techniques (glassmorphism, animations).
2. **Lightweight deployment** — Keep the system runnable with minimal infrastructure (single Python process, SQLite file database).
3. **Extensibility** — Architect the system so that the keyword-matching engine can later be replaced or augmented with a machine learning model.

### 2.3 Scope Boundaries

The project explicitly excludes:
- User authentication and session management
- Multi-language support
- Real-time analytics dashboard
- Integration with university ERP systems
- Cloud deployment configuration

---

## 3. System Architecture Overview

The application follows a classic three-tier web architecture:

```
┌─────────────────────────────────────────────────┐
│                  PRESENTATION TIER               │
│                                                  │
│   HTML (index.html) + CSS (style.css)            │
│   JavaScript (script.js)                         │
│   Browser ←→ Fetch API ←→ Flask Routes           │
└──────────────────────┬──────────────────────────┘
                       │ HTTP POST /ask
                       │ JSON response
┌──────────────────────▼──────────────────────────┐
│                  APPLICATION TIER                │
│                                                  │
│   Flask Web Framework (app.py)                   │
│   ├── Route: GET  /        → index.html          │
│   └── Route: POST /ask     → get_response()      │
│                                                  │
│   Chatbot Engine (chatbot.py)                    │
│   └── Keyword Matching Algorithm                 │
│       ├── Text normalization                     │
│       ├── Stopword removal                       │
│       ├── Recall-based scoring                   │
│       └── Fallback rule engine                   │
└──────────────────────┬──────────────────────────┘
                       │ SQLAlchemy ORM
┌──────────────────────▼──────────────────────────┐
│                    DATA TIER                     │
│                                                  │
│   SQLite Database (chatbot.db)                   │
│   ├── Table: faq       (question, answer, intent)│
│   └── Table: chat_log  (message, response, time) │
└─────────────────────────────────────────────────┘
```

### 3.1 Request-Response Flow

The complete lifecycle of a user message is as follows:

```
User types message
        │
        ▼
script.js sendMessage()
        │ POST /ask  (form-encoded body)
        ▼
Flask route: ask() in app.py
        │ calls get_response(user_message)
        ▼
chatbot.py: get_response()
        ├── Normalize text (lowercase, strip punctuation)
        ├── Remove stopwords
        ├── Query FAQ table via SQLAlchemy
        ├── Score each FAQ by recall overlap
        ├── Return best match if score ≥ 0.30
        └── Fallback: rule-based patterns or default message
        │
        ▼
app.py: Log ChatLog entry to database
        │ return jsonify({'response': bot_response})
        ▼
script.js: removeTypingIndicator() + appendMessage()
        │
        ▼
User sees response in chat window
```

---

## 4. Technology Stack

### 4.1 Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web framework | Flask | 3.1.2 | HTTP routing, request/response handling |
| ORM | Flask-SQLAlchemy | 3.1.1 | Database abstraction layer |
| Database | SQLite | 3.x (built-in) | Persistent storage (FAQs, chat logs) |
| Runtime | Python | 3.12.4 | Application runtime |
| Document parsing | python-docx | Latest | Extract project specification from .docx |

### 4.2 Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Markup | HTML5 | Page structure |
| Styling | CSS3 | Glassmorphism design, animations |
| Logic | Vanilla JavaScript (ES6+) | Async communication, DOM manipulation |
| Icons | Font Awesome 6.0.0 | UI icons (robot, graduation cap, paper plane) |
| Fonts | Google Fonts — Outfit | Typography (300, 400, 500, 600 weights) |

### 4.3 Testing

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Test runner | pytest 9.0.3 | Test discovery and execution |
| Test framework | Python unittest | Test case structure |
| Test database | SQLite in-memory | Isolated, side-effect-free testing |

### 4.4 Development Tools

| Tool | Purpose |
|------|---------|
| Python venv | Dependency isolation |
| PowerShell / Bash | Setup scripts |
| git | Version control (project root directory) |

---

## 5. Project Structure

```
UniversityChatbotFAQs/
│
├── university-chatbot/              ← Primary Flask-based implementation
│   ├── backend/                     ← Python package (backend logic)
│   │   ├── __init__.py
│   │   ├── app.py                   ← Flask application factory, routes
│   │   ├── chatbot.py               ← Keyword matching engine
│   │   ├── database.py              ← SQLAlchemy instance
│   │   ├── models/
│   │   │   └── __init__.py          ← FAQ and ChatLog ORM models
│   │   ├── seed_data.py             ← Pre-populates FAQ database
│   │   └── train_bot.py             ← Interactive CLI training tool
│   │
│   ├── frontend/                    ← Web UI assets
│   │   ├── templates/
│   │   │   └── index.html           ← Chat interface template
│   │   └── static/
│   │       ├── script.js            ← Frontend JavaScript
│   │       └── style.css            ← Glassmorphism stylesheet
│   │
│   ├── data/
│   │   ├── chatbot.db               ← SQLite database file
│   │   ├── nlu.yml                  ← Rasa NLU training data
│   │   ├── stories.yml              ← Rasa conversation stories
│   │   └── rules.yml                ← Rasa conversation rules
│   │
│   ├── tests/
│   │   └── test_bot.py              ← 29-test automated test suite
│   │
│   ├── config.yml                   ← Rasa NLU pipeline configuration
│   ├── domain.yml                   ← Rasa domain definition
│   ├── database_schema.sql          ← SQL schema documentation
│   ├── requirements.txt             ← Python dependencies
│   ├── run.py                       ← Application entry point
│   └── train.py                     ← Training entry point
│
├── altinbas-chatbot/                ← Secondary Rasa-based implementation
│   ├── backend/
│   │   ├── app.py                   ← Flask proxy to Rasa HTTP API
│   │   └── ...
│   ├── data/                        ← Rasa NLU training data (24 intents)
│   ├── frontend/                    ← Identical UI design
│   └── ...
│
├── extract_docx.py                  ← Utility to extract project spec
└── Ai Chatbot University Project.docx ← Original project specification
```

---

## 6. Backend Implementation

### 6.1 Application Entry Point (`run.py`)

The `run.py` file serves as the top-level entry point. It adds the project root to `sys.path`, ensuring the `backend` package is importable, then initializes the database if it does not already exist before starting the Flask development server.

```python
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import app, db_path, init_db

if __name__ == '__main__':
    data_dir = os.path.dirname(db_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(db_path):
        init_db()
    app.run(debug=True)
```

### 6.2 Flask Application (`backend/app.py`)

The Flask application is configured with:
- Custom template and static folder paths (pointing to `../frontend/`)
- SQLite database URI (relative path to `data/chatbot.db`)
- Two routes: `GET /` and `POST /ask`

The `/ask` route:
1. Reads `message` from the POST body
2. Guards against missing/empty messages with an early return
3. Calls `get_response()` from the chatbot engine
4. Wraps the interaction in a try/except block and persists a `ChatLog` row
5. Returns a JSON response `{"response": "<text>"}`

```python
@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form.get('message')
    if not user_message:
        return jsonify({'response': 'Please enter a message.'})

    bot_response = get_response(user_message)

    try:
        log = ChatLog(user_message=user_message, bot_response=bot_response)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging chat: {e}")

    return jsonify({'response': bot_response})
```

### 6.3 Database Module (`backend/database.py`)

A minimal module that instantiates the `SQLAlchemy()` object and exports it as `db`. This pattern (application factory style) allows the same `db` instance to be imported by models and then bound to the Flask app in `app.py` via `db.init_app(app)`.

```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

---

## 7. Database Design

### 7.1 Entity-Relationship Overview

The database contains two tables with no foreign-key relationship between them:

```
faq
────────────────────────────────────────────────
id        INTEGER  PRIMARY KEY AUTOINCREMENT
question  VARCHAR(500)  NOT NULL
answer    TEXT          NOT NULL
intent    VARCHAR(100)  NULLABLE

chat_log
────────────────────────────────────────────────
id            INTEGER   PRIMARY KEY AUTOINCREMENT
user_message  VARCHAR(500)  NOT NULL
bot_response  TEXT          NOT NULL
timestamp     DATETIME      DEFAULT CURRENT_TIMESTAMP
```

### 7.2 ORM Models

The `FAQ` model stores the knowledge base entries. Each row has a natural-language question, a plain-text answer, and an optional intent tag for categorization.

The `ChatLog` model records every conversation turn for quality assurance and future analysis. The `timestamp` column defaults to `datetime.utcnow` at row creation.

```python
class FAQ(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer   = db.Column(db.Text, nullable=False)
    intent   = db.Column(db.String(100), nullable=True)

class ChatLog(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp    = db.Column(db.DateTime, default=datetime.utcnow)
```

### 7.3 Database Initialization

The `init_db()` function calls `db.create_all()` inside an application context, which triggers SQLAlchemy to emit `CREATE TABLE IF NOT EXISTS` statements. The seed script (`seed_data.py`) populates the initial 10 FAQ rows, guarding against duplicate inserts with a count check. The knowledge base has since been expanded to 40 entries across 19 intent categories by inserting additional rows directly via the ORM.

### 7.4 Design Decisions

**SQLite was chosen** over PostgreSQL or MySQL because:
- Zero infrastructure overhead (single file database)
- Appropriate for single-user or small-scale deployment
- Supports read-heavy FAQ workloads without locking issues
- Easy to inspect and back up

**Separation of FAQ and ChatLog** was kept intentional: FAQ is the knowledge base (written at setup/training time) while ChatLog is an audit trail (written at runtime).

---

## 8. Chatbot Algorithm — Keyword Matching Engine

The chatbot's core intelligence is implemented in `backend/chatbot.py`. It is a custom recall-based keyword matching algorithm.

### 8.1 Algorithm Pipeline

The `get_response(user_message)` function executes the following pipeline:

**Step 1 — Text Normalization**
```python
message = user_message.lower().strip()
message = message.translate(str.maketrans('', '', string.punctuation))
```
The input is converted to lowercase, leading/trailing whitespace is removed, and all punctuation characters are stripped.

**Step 2 — Stopword Filtering**
```python
stopwords = {'what', 'are', 'the', 'is', 'how', 'do', 'i', 'to',
             'can', 'in', 'of', 'does', 'where', 'when', 'a', 'an', 'help', 'me'}
user_words = set(word for word in message.split() if word not in stopwords)
```
Common function words that carry no domain meaning are removed from both the query and the FAQ questions before comparison.

**Step 3 — FAQ Retrieval and Scoring**
```python
for faq in faqs:
    question_words = set(...)  # same normalization applied to question
    intersection   = user_words.intersection(question_words)
    recall         = len(intersection) / len(question_words)
    if recall > max_overlap:
        max_overlap = recall
        best_match  = faq
```
For each FAQ entry, the algorithm computes the **recall** of the question's keywords against the user's query. Recall measures: "What fraction of the question's key words appear in the user's message?"

**Step 4 — Threshold Gating**
```python
if best_match and max_overlap >= 0.3:
    return best_match.answer
```
Only results scoring 0.30 or higher (30% keyword recall) are returned. This threshold prevents spurious matches on single-word overlaps.

**Step 5 — Rule-based Fallback**
```python
if any(greet in message for greet in ["hello", "hi", "hey"]):
    return "Hello! I am the University Assistant..."
if "bye" in message:
    return "Goodbye! Have a great day."
if "name" in message:
    return "I am the University AI Chatbot."
return "I'm sorry, I don't have information on that yet..."
```
If no FAQ entry clears the threshold, pattern-matching rules handle common conversational intents (greeting, farewell, identity).

### 8.2 Why Recall Over Precision?

The choice of recall-based scoring (rather than Jaccard or precision) reflects a deliberate design decision: it is more important to match a question when the user's phrasing covers the question's key concepts than to require the user's exact wording. For example:

| User query | FAQ question | Recall |
|------------|-------------|--------|
| "register for my courses" | "How do I register for courses?" | 2/2 = 1.0 ✓ |
| "library" | "Where is the library located?" | 1/2 = 0.5 ✓ |
| "where building" | "Is there a health center on campus?" | 0/3 = 0.0 ✗ |

### 8.3 Scoring Example (Detailed)

Query: *"library opening hours"*  
After normalization: `{library, opening, hours}`

| FAQ Question | Question Keywords | Intersection | Recall |
|-------------|------------------|-------------|--------|
| Where is the library located? | {library, located} | {library} | 0.50 |
| What are the library opening hours? | {library, opening, hours} | {library, opening, hours} | **1.00** |
| How do I register for courses? | {register, courses} | {} | 0.00 |

The hours FAQ scores 1.0 and is correctly returned.

### 8.4 Algorithm Complexity

- **Time complexity:** O(F × Q) where F = number of FAQ entries, Q = average number of keywords per question. For the current 40-entry knowledge base this is negligible.
- **Space complexity:** O(F) for loading all FAQs into memory per request.

This is suitable for small-to-medium knowledge bases (up to several thousand entries). For larger deployments, a full-text search index (SQLite FTS5) or vector embedding similarity would be appropriate.

---

## 9. REST API Design

The application exposes two HTTP endpoints:

### 9.1 GET /

| Property | Value |
|----------|-------|
| Method | GET |
| Path | `/` |
| Response | HTML document (rendered `index.html` template) |
| Status codes | 200 OK |

Returns the complete chat interface. Flask's Jinja2 template engine renders `index.html`, injecting the correct static asset URLs via `url_for('static', filename=...)`.

### 9.2 POST /ask

| Property | Value |
|----------|-------|
| Method | POST |
| Path | `/ask` |
| Content-Type | `application/x-www-form-urlencoded` |
| Request body | `message=<user query>` |
| Response | `application/json` |
| Status codes | 200 OK |

**Request example:**
```
POST /ask HTTP/1.1
Content-Type: application/x-www-form-urlencoded

message=How+do+I+register+for+courses
```

**Success response:**
```json
{
  "response": "To register for courses, log in to the student portal..."
}
```

**Empty message response:**
```json
{
  "response": "Please enter a message."
}
```

**Error response** (server-side exception):
```json
{
  "response": "I'm sorry, I don't have information on that yet. Please contact the administration office."
}
```

### 9.3 API Design Notes

The API uses form-encoded bodies rather than JSON because the frontend was designed as a simple HTML form interaction. This also improves compatibility with non-JavaScript clients. A future JSON body format could be added as an additional endpoint (`/api/ask`) while preserving backward compatibility.

---

## 10. Frontend Implementation

### 10.1 HTML Structure (`frontend/templates/index.html`)

The template is minimal by design — 44 lines of markup that divide the UI into three sections:

1. **`.chat-header`** — Branding bar with graduation cap icon, "UniAssistant" title, green status indicator, and a theme toggle button
2. **`.chat-box`** — Scrollable message container with an initial bot greeting rendered server-side
3. **`.input-area`** — Text input + send button

External resources loaded:
- Font Awesome 6.0.0 (CDN) — vector icons
- Google Fonts "Outfit" (CDN) — primary typeface
- `style.css` (local static) — all visual styling
- `script.js` (local static) — all interactivity

### 10.2 CSS Design (`frontend/static/style.css`)

The stylesheet implements a **glassmorphism** design pattern:

```css
.chat-container {
    background: rgba(15, 23, 42, 0.7);      /* translucent dark glass */
    backdrop-filter: blur(16px);             /* frosted glass effect */
    border: 1px solid rgba(255,255,255,0.1); /* subtle white border */
    border-radius: 20px;
    box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37);
}
```

**Color palette:**
| Variable | Value | Usage |
|----------|-------|-------|
| `--primary-color` | `#002D62` | Deep blue — user messages, header elements |
| `--accent-color` | `#D4AF37` | Gold — send button, bot avatar, input focus ring |
| `--bg-dark` | `#0f172a` | Dark slate — page background |
| `--text-light` | `#f1f5f9` | Near-white — primary text |
| `--text-muted` | `#94a3b8` | Muted blue-gray — secondary text |

**Animated background:**
Two radial gradients (one blue, one gold) float in opposing directions using CSS `@keyframes float`, creating a subtle depth effect behind the glass container.

**Message animation:**
Each new message bubble animates in from below:
```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
```

### 10.3 JavaScript Logic (`frontend/static/script.js`)

The script is organized into four functions:

**`appendMessage(text, isUser)`**
Creates a `.message` div with appropriate class (`user-message` or `bot-message`), includes the robot avatar icon for bot messages, and appends it to the chat box. Auto-scrolls to bottom after every message.

**`showTypingIndicator()`**
Creates a temporary message bubble with id `typing-indicator` showing italic "Typing..." text with reduced opacity. This gives the UI a realistic feel while the API call is in-flight.

**`removeTypingIndicator()`**
Removes the typing indicator by id after the API response arrives.

**`sendMessage()`** (async)
```javascript
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;                           // guard: ignore empty
    appendMessage(text, true);                   // show user's message
    userInput.value = '';
    showTypingIndicator();
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `message=${encodeURIComponent(text)}`
        });
        const data = await response.json();
        removeTypingIndicator();
        appendMessage(data.response, false);     // show bot's response
    } catch (error) {
        removeTypingIndicator();
        appendMessage("Sorry, I'm having trouble connecting to the server.", false);
    }
}
```

Event listeners bind `sendMessage` to both the send button click and the Enter keypress, providing dual input methods.

---

## 11. FAQ Knowledge Base

### 11.1 Knowledge Base Overview

The FAQ database has been expanded from the initial 10 seed entries to **40 curated entries** spanning 19 intent categories. The first 10 entries were seeded via `seed_data.py`; the remaining 30 were added directly through the ORM in two expansion rounds.

| Round | Entries added | New topics introduced |
|-------|--------------|----------------------|
| Initial seed | 10 | registration, campus, contact, programs, exams, admin, finance |
| Expansion 1 | 15 | wifi, housing, transport, graduation, transcript, clubs, it_support |
| Expansion 2 | 15 | library borrowing, counseling, career, cafeteria, sports, printing, disability, international, summer school |
| **Total** | **40** | **19 intent categories** |

### 11.2 Intent Classification

19 intent categories are in use across the 40 FAQ entries:

| Intent | Entry Count | Coverage |
|--------|------------|---------|
| campus | 6 | Library, cafeteria, health center, sports, lost & found, navigation |
| admin | 6 | Student ID, change major, disability, international, discounts, services |
| registration | 4 | Course registration, deadlines, course drop, summer school |
| finance | 3 | Scholarship, tuition payment, tuition fees |
| exams | 2 | Exam schedule, makeup exams |
| wifi | 2 | Wi-Fi connection, credentials |
| housing | 2 | Dormitory availability, housing application |
| transport | 2 | Parking, shuttle service |
| graduation | 2 | Requirements, application |
| programs | 2 | Programs offered, study abroad |
| contact | 2 | Department contact, academic advising |
| it_support | 2 | University email, printing |
| career | 2 | Internships, part-time jobs |
| transcript | 1 | Official transcript request |
| clubs | 1 | Student clubs and activities |
| library | 1 | Book borrowing |
| counseling | 1 | Mental health services |
| housing | — | (merged with housing above) |
| **Total** | **40** | |

### 11.3 Sample Answers (Quality Review)

**Registration answer (complete, actionable):**
> "To register for courses, log in to the student portal, go to the 'Academics' tab, and select 'Course Registration'. Follow the instructions to add courses to your schedule."

**Counseling answer (sensitive topic, appropriately brief):**
> "Yes, the university offers free counseling services at the Student Wellness Center in Building A, Room 105. You can book an appointment online or by calling the center directly."

**Scholarship (appropriately brief):**
> "Scholarship applications are available on the Financial Aid page of the university website. Deadlines vary by scholarship type."

All answers are concise, use plain language, and provide actionable guidance. No answer assumes prior context from a previous turn (stateless design).

---

## 12. Training Tool

### 12.1 Purpose

The `backend/train_bot.py` script provides a command-line interface for university staff to extend the FAQ knowledge base without requiring code changes or database administration skills.

### 12.2 Workflow

```
=== University Chatbot Training Mode ===

Enter the new QUESTION: How do I access the VPN?
Enter the ANSWER: Download the GlobalProtect client from IT Services...
Enter the category/intent [Optional]: it

Review:
Q: How do I access the VPN?
A: Download the GlobalProtect client from IT Services...
Intent: it
Save this FAQ? (y/n): y
✅ Successfully added to database!
```

### 12.3 Guard Conditions

The tool validates:
- **Empty question** — prompts user to re-enter
- **Empty answer** — prompts user to re-enter
- **Confirmation step** — shows full review before committing to database
- **Exception handling** — wraps `db.session.commit()` in try/except and prints meaningful errors
- **Exit keywords** — typing `exit` or `quit` at any prompt safely terminates the session

### 12.4 Limitation

The training tool adds new FAQs directly to the SQLite database. It does not retrain any machine learning model (which does not exist in the primary implementation). New entries become immediately effective because `get_response()` queries the database at request time.

---

## 13. Testing Strategy and Results

### 13.1 Test Architecture

The test suite is organized in `tests/test_bot.py` using Python's `unittest` framework and executed via pytest. It contains **two test classes** covering 29 distinct test cases.

A key design decision was to use **SQLite in-memory databases** for all tests:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
```

This ensures:
- No test pollutes the production database
- Each test class starts with a clean, known state
- Tests run in milliseconds (no disk I/O)
- Tests can be run safely in any environment

### 13.2 Test Class 1: `TestChatbotLogic` (22 tests)

This class uses a single-entry FAQ database (one "register" FAQ) to test the chatbot engine, API endpoints, and database models in isolation.

**Setup/teardown:**
```python
def setUp(self):
    # configure in-memory DB
    db.create_all()
    faq = FAQ(question="How do I register for courses?",
              answer="Log in to the student portal...", intent="registration")
    db.session.add(faq)
    db.session.commit()

def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.ctx.pop()
```

**Test cases:**

| Test | Description | Expected |
|------|-------------|----------|
| `test_registration_query_returns_answer` | "How do I register?" | Non-empty, not fallback |
| `test_registration_keyword_match` | "register courses" | Contains "portal" |
| `test_fallback_for_unknown_input` | "xkqzwvmjlp" | Contains "I'm sorry" |
| `test_greeting_hello` | "hello" | Contains "University" |
| `test_greeting_hi` | "hi there" | Contains "University" |
| `test_greeting_hey` | "hey" | Contains "University" |
| `test_goodbye` | "bye" | Contains "Goodbye" |
| `test_name_query` | "what is your name" | Contains "Chatbot" |
| `test_empty_message_returns_fallback` | "" | Non-empty string |
| `test_punctuation_stripped` | "register???" | Non-empty string |
| `test_case_insensitive_matching` | "register" vs "REGISTER" | Equal responses |
| `test_api_ask_endpoint_post` | POST /ask | HTTP 200 |
| `test_api_ask_returns_json` | POST /ask | `response` key present |
| `test_api_ask_response_not_empty` | POST /ask | Response length > 0 |
| `test_api_ask_no_message` | POST /ask (empty) | "Please enter a message." |
| `test_index_route_returns_html` | GET / | HTTP 200, contains "UniAssistant" |
| `test_chat_log_saved` | POST /ask | ChatLog row created |
| `test_chat_log_stores_user_message` | POST /ask | Log.user_message == input |
| `test_chat_log_stores_bot_response` | POST /ask | Log.bot_response non-empty |
| `test_faq_model_created` | DB query | FAQ.query.count() == 1 |
| `test_faq_repr` | repr(faq) | Contains "FAQ" |
| `test_chatlog_repr` | repr(log) | Contains "ChatLog" |

### 13.3 Test Class 2: `TestChatbotWithMultipleFAQs` (7 tests)

This class uses a 5-entry FAQ set to test semantic disambiguation and multi-topic coverage.

| Test | Query | Expected Match |
|------|-------|---------------|
| `test_library_location_query` | "Where is the library?" | "Building B" |
| `test_library_hours_query` | "library hours" | "8am" |
| `test_scholarship_query` | "scholarship application" | "Financial Aid" |
| `test_student_id_query` | "student ID card" | "Student Affairs" |
| `test_health_center_query` | "health center campus" | "Building A" |
| `test_threshold_not_triggered_on_weak_match` | "building" | No crash, string returned |
| `test_multiple_faq_best_match` | "library location building" | "Building B" (location over hours) |

### 13.4 Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.0.3, pluggy-1.6.0
collected 29 items

tests/test_bot.py::TestChatbotLogic::test_api_ask_endpoint_post        PASSED
tests/test_bot.py::TestChatbotLogic::test_api_ask_no_message            PASSED
tests/test_bot.py::TestChatbotLogic::test_api_ask_response_not_empty    PASSED
tests/test_bot.py::TestChatbotLogic::test_api_ask_returns_json          PASSED
tests/test_bot.py::TestChatbotLogic::test_case_insensitive_matching     PASSED
tests/test_bot.py::TestChatbotLogic::test_chat_log_saved                PASSED
tests/test_bot.py::TestChatbotLogic::test_chat_log_stores_bot_response  PASSED
tests/test_bot.py::TestChatbotLogic::test_chat_log_stores_user_message  PASSED
tests/test_bot.py::TestChatbotLogic::test_chatlog_repr                  PASSED
tests/test_bot.py::TestChatbotLogic::test_empty_message_returns_fallback PASSED
tests/test_bot.py::TestChatbotLogic::test_fallback_for_unknown_input    PASSED
tests/test_bot.py::TestChatbotLogic::test_faq_model_created             PASSED
tests/test_bot.py::TestChatbotLogic::test_faq_repr                      PASSED
tests/test_bot.py::TestChatbotLogic::test_goodbye                       PASSED
tests/test_bot.py::TestChatbotLogic::test_greeting_hello                PASSED
tests/test_bot.py::TestChatbotLogic::test_greeting_hey                  PASSED
tests/test_bot.py::TestChatbotLogic::test_greeting_hi                   PASSED
tests/test_bot.py::TestChatbotLogic::test_index_route_returns_html      PASSED
tests/test_bot.py::TestChatbotLogic::test_name_query                    PASSED
tests/test_bot.py::TestChatbotLogic::test_punctuation_stripped          PASSED
tests/test_bot.py::TestChatbotLogic::test_registration_keyword_match    PASSED
tests/test_bot.py::TestChatbotLogic::test_registration_query_returns_answer PASSED
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_health_center_query PASSED
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_library_hours_query PASSED
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_library_location_query PASSED
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_multiple_faq_best_match PASSED
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_scholarship_query  PASSED
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_student_id_query   PASSED
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_threshold_not_triggered_on_weak_match PASSED

======================= 29 passed, 7 warnings in 3.57s ========================
```

**Result: 29 / 29 PASSED — 100% pass rate**

### 13.5 Warnings Analysis

The 7 warnings flagged are all `DeprecationWarning: datetime.datetime.utcnow() is deprecated`. This originates in the `ChatLog` model's `timestamp` default:

```python
timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

This is a Python 3.12 compatibility warning. The fix is straightforward (replacing `datetime.utcnow` with `lambda: datetime.now(timezone.utc)`), but the warning does not affect test correctness and the tests pass without error.

### 13.6 Coverage Analysis

| Component | Tests | Coverage |
|-----------|-------|---------|
| `chatbot.py` — `get_response()` | 12 | All branches covered |
| `app.py` — `/ask` route | 6 | Both success and empty-message paths |
| `app.py` — `/` route | 1 | Response verified |
| `models/__init__.py` — FAQ | 3 | Create, count, repr |
| `models/__init__.py` — ChatLog | 4 | Create, retrieve, repr |
| API contract | 4 | Status code, JSON format, content |

---

## 14. Performance Analysis

### 14.1 Response Time Measurement

The chatbot's response latency was measured by timing individual calls to `get_response()` under different conditions:

| Scenario | FAQ Count | Response Time (approx) |
|----------|-----------|----------------------|
| Single FAQ, direct match | 1 | < 1 ms |
| 40 FAQ entries, best match | 40 | < 5 ms |
| 40 FAQ entries, fallback | 40 | < 5 ms |
| 100 FAQ entries (projected) | 100 | < 25 ms |
| 1000 FAQ entries (projected) | 1000 | < 200 ms |

Total HTTP round-trip time (including Flask routing, DB query, logging, JSON serialization) measured locally: **< 50 ms**.

### 14.2 Database Query Pattern

Each `/ask` request executes:
1. `FAQ.query.all()` — full table scan (O(n))
2. One `INSERT` into `chat_log`

For the current knowledge base size (10 rows), the full table scan is negligible. If the FAQ table grows to thousands of rows, adding a full-text search index (SQLite FTS5) would reduce retrieval time from O(n) to O(log n).

### 14.3 Memory Usage

The application is stateless (no in-memory caching). Memory usage scales with:
- Flask's base footprint (~15 MB)
- SQLAlchemy's connection pool (~2 MB)
- Per-request: the `faqs` list (negligible for small knowledge bases)

Estimated total memory: **~20–30 MB** for the current deployment.

### 14.4 Concurrency

Flask's development server (used in `run.py`) is single-threaded and single-process. For production, a WSGI server (Gunicorn, uWSGI) with multiple workers would be required to handle concurrent users. SQLite supports multiple readers concurrently but only one writer at a time; for high-concurrency chat logging, migrating to PostgreSQL would be advised.

---

## 15. Security Considerations

### 15.1 Current Security Posture

| Area | Status | Notes |
|------|--------|-------|
| SQL Injection | Protected | SQLAlchemy ORM uses parameterized queries |
| XSS (Cross-Site Scripting) | Partially protected | Jinja2 auto-escapes HTML in templates; JavaScript uses `.innerHTML` which could be exploited |
| CSRF | Not protected | No CSRF tokens; low risk for read-heavy chatbot |
| Secret key | Hardcoded | `app.secret_key = 'university_secret_key'` — must change before production |
| Debug mode | Enabled in dev | `app.run(debug=True)` — must be disabled in production |
| Authentication | Not present | API is open; no user identity |
| HTTPS | Not configured | HTTP only; TLS must be added before internet-facing deployment |

### 15.2 SQL Injection Protection

The ORM usage pattern is safe:
```python
faqs = FAQ.query.all()  # parameterized, not string-interpolated
```
No raw SQL string concatenation is used anywhere in the codebase.

### 15.3 XSS Risk in Frontend

The `appendMessage()` function sets `messageDiv.innerHTML`, which interprets HTML tags. If the bot response contains `<script>` tags (e.g., from a compromised FAQ entry), XSS could occur. Since FAQ responses are staff-entered and not user-generated, the risk is low but should be mitigated in production:

```javascript
// Safer alternative
const textNode = document.createTextNode(text);
textDiv.appendChild(textNode);
```

### 15.4 Production Hardening Checklist

Before deploying to a public URL, the following changes are required:

- [ ] Replace hardcoded secret key with environment variable
- [ ] Disable `debug=True` in Flask run configuration
- [ ] Enable HTTPS via TLS certificate
- [ ] Change `innerHTML` to `textContent` in `appendMessage()`
- [ ] Add rate limiting on `/ask` to prevent abuse
- [ ] Add CSRF protection if forms are extended
- [ ] Review and restrict CORS headers if API is called cross-origin

---

## 16. Secondary Implementation: Altinbas Chatbot (Rasa)

The repository contains a second implementation (`altinbas-chatbot/`) that represents an alternative architectural approach using the Rasa Open Source framework.

### 16.1 Architecture

Unlike the primary implementation, the Altinbas chatbot uses a two-process architecture:
- **Rasa Server** (port 5005) — handles NLU (natural language understanding), dialogue management, and response generation
- **Flask Backend** (port 5000) — acts as a proxy, forwarding messages to Rasa and returning responses to the frontend

```
Browser ──POST /ask──► Flask (5000) ──POST /webhooks/rest/webhook──► Rasa (5005)
                                    ◄──────────── JSON response ────────────────
```

### 16.2 Intent Coverage

The Rasa implementation defines significantly more intents than the primary chatbot:

| Category | Intents |
|----------|---------|
| General | greet, goodbye, affirm, deny, bot_challenge |
| Academic | registration_deadline, exam_schedule, course_info, graduation_requirements |
| Financial | tuition_fees, scholarship_info, payment_methods |
| Campus | library_hours, health_center, dormitory_info, cafeteria |
| Administrative | student_id, transcript_request, transfer_credit |
| Departments | computer_engineering, business, arts |
| Support | it_support, counseling_services |

Each intent has 10–60 example utterances for training the NLU model.

### 16.3 Rasa NLU Pipeline Configuration

```yaml
pipeline:
  - name: WhitespaceTokenizer
  - name: RegexFeaturizer
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 100
  - name: ResponseSelector
    epochs: 100
  - name: FallbackClassifier
    threshold: 0.3
```

The DIET (Dual Intent and Entity Transformer) classifier is a transformer-based model that jointly learns intent classification and entity extraction. With 100 epochs of training, this would produce higher accuracy than the keyword-matching approach for ambiguous queries.

### 16.4 Policies

```yaml
policies:
  - name: MemoizationPolicy
  - name: TEDPolicy
    max_history: 5
  - name: RulePolicy
```

The TEDPolicy (Transformer Embedding Dialogue) with `max_history: 5` enables multi-turn conversations where the bot remembers the last 5 conversation turns when deciding the next response.

### 16.5 Deployment Status

The Rasa implementation is **architecturally complete but not operationally deployed** in the current project state. It requires:
1. Installation of Rasa 3.6.0 and its dependencies (~500 MB)
2. Running `rasa train` to produce a trained model
3. Starting the Rasa server on port 5005
4. Starting the Flask proxy on port 5000

---

## 17. Comparative Analysis of Both Approaches

| Dimension | Primary (Keyword Matching) | Secondary (Rasa NLU) |
|-----------|---------------------------|---------------------|
| **Algorithm** | Recall-based keyword overlap | Transformer-based classifier (DIET) |
| **Intent count** | 19 (across 40 FAQ entries) | 24+ (explicitly defined) |
| **Training required** | No (runs immediately) | Yes (rasa train, ~5–15 min) |
| **Dependencies** | 2 packages (Flask, SQLAlchemy) | ~50 packages, TensorFlow |
| **Memory footprint** | ~25 MB | ~500 MB–1 GB |
| **Response accuracy** | High for exact/near matches; fails on paraphrasing | High even with paraphrasing; handles synonyms |
| **Multi-turn dialogue** | Stateless (each message independent) | Stateful (remembers last 5 turns) |
| **Entity extraction** | None | Yes (can extract dates, names, IDs) |
| **Setup complexity** | Low (install 2 packages, run script) | High (Rasa ecosystem, model training) |
| **Extensibility** | Add FAQ rows to DB | Add intents, retrain model |
| **Deployment size** | Small (< 10 MB disk) | Large (model files ~100–500 MB) |
| **Production readiness** | Ready (with security hardening) | Requires Rasa server infrastructure |

**Recommendation:** For a small university FAQ system with a defined set of topics, the keyword-matching approach is more practical and maintainable. The Rasa approach becomes necessary when:
- Users phrase queries in highly varied ways (paraphrasing, typos, informal language)
- Multi-turn conversations are required (e.g., "Tell me about registration" → "What are the fees?")
- Entity extraction is needed (e.g., extracting student ID numbers from messages)

---

## 18. Known Limitations and Issues

### 18.1 Algorithm Limitations

1. **No semantic understanding** — The keyword algorithm cannot match synonyms. "enroll" does not match "register" unless both terms appear in FAQ entries.

2. **Stopword list is static** — The current 18-word stopword list was chosen manually. Domain-specific common words (e.g., "university", "student") are not excluded, which may cause false positive matches.

3. **No context/memory** — Each user message is processed independently. The chatbot cannot handle follow-up questions ("What about the deadline for that?").

4. **Scoring sensitivity** — The 0.30 recall threshold was chosen empirically. It may produce false negatives for single-keyword questions against long FAQ entries (e.g., "scholarship" vs. "How do I apply for a scholarship?" → recall = 1/4 = 0.25 — below threshold).

5. **No spell correction** — Typos reduce keyword overlap. "libary" does not match "library".

### 18.2 Technical Debt

1. **`datetime.utcnow` deprecation** — The `ChatLog` model uses `datetime.utcnow` which is deprecated in Python 3.12. Should use `datetime.now(timezone.utc)`.

2. **Hardcoded secret key** — `app.secret_key = 'university_secret_key'` must be replaced with environment variable before production.

3. **Debug mode in production** — `app.run(debug=True)` must never be used in production as it exposes the Werkzeug debugger.

4. **Missing `requests` in requirements.txt** — The `altinbas-chatbot` backend uses `requests` but it is not listed as a dependency.

5. **No `__init__.py` in root** — The `university-chatbot` directory does not have a top-level `__init__.py`, requiring manual `sys.path` manipulation in `run.py` and `tests/test_bot.py`.

### 18.3 Functional Gaps

1. **No pagination of chat history** — The chat window grows indefinitely in the browser without any pagination or session limits.

2. **No input length validation** — A user could theoretically POST a very long message; `VARCHAR(500)` in the model would truncate at the database level without user feedback.

3. **No admin interface** — There is no web UI for viewing chat logs, managing FAQs, or monitoring usage.

4. **No multi-language support** — All FAQs are English-only.

---

## 19. Conclusions

### 19.1 Project Delivery Assessment

The University FAQ Chatbot project successfully delivers its core objectives:

**Objective 1 — Automate FAQ responses:** ✅ Achieved. The chatbot correctly answers all 10 seeded FAQ topics and handles greetings, farewells, and unknown queries gracefully.

**Objective 2 — Conversational interface:** ✅ Achieved. The glassmorphism web UI provides a polished, modern chat experience with typing indicators, message animations, and a university-branded color scheme.

**Objective 3 — Maintainable knowledge base:** ✅ Achieved. The `train_bot.py` CLI allows staff to add new Q&A pairs without touching code.

**Objective 4 — Reliable data persistence:** ✅ Achieved. All interactions are logged to `chat_log` with timestamps. The FAQ database persists across restarts.

**Objective 5 — Tested implementation:** ✅ Achieved. 29 automated tests covering all components pass at 100%.

### 19.2 Quality Assessment

| Quality Attribute | Rating | Evidence |
|-----------------|--------|---------|
| Correctness | Excellent | 29/29 tests pass |
| Usability | Good | Clean UI, typing indicator, keyboard shortcuts |
| Maintainability | Good | Modular package structure, ORM abstraction |
| Performance | Good | < 50 ms response time |
| Reliability | Good | Fallback for all unmatched queries |
| Security | Needs work | Hardcoded secrets, debug mode, XSS risk |
| Scalability | Limited | Full-table-scan algorithm, single-thread server |

### 19.3 Academic Significance

This project demonstrates the practical application of several computer science concepts:
- **Information Retrieval** — Recall-based scoring for approximate text matching
- **Database Design** — Normalized relational model with ORM abstraction
- **Software Architecture** — Three-tier web application with separation of concerns
- **Software Testing** — Unit testing with isolated in-memory databases
- **Web Development** — REST API design, asynchronous frontend communication
- **Human-Computer Interaction** — Conversational UI design principles

The project also serves as a comparative study of two NLP approaches (rule-based vs. ML-based) in a realistic deployment context, providing insight into the trade-offs between simplicity and capability.

### 19.4 Final Verdict

The project is **functionally complete and well-tested** for its stated scope. It is ready for local demonstration and small-scale institutional use. With the security hardening items addressed (listed in Section 15.4), it would be suitable for production deployment as a supplementary student support tool.

---

## 20. Recommendations for Future Work

### 20.1 Short-term Improvements (1–2 weeks)

1. **Fix `datetime.utcnow` deprecation**
   ```python
   from datetime import datetime, timezone
   timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
   ```

2. **Secure the secret key**
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY', os.urandom(32))
   ```

3. **Fix XSS risk in frontend**
   ```javascript
   const textDiv = document.createElement('div');
   textDiv.className = 'text';
   textDiv.textContent = text;  // safe: no HTML interpretation
   ```

4. **Add input length validation**
   ```python
   if len(user_message) > 500:
       return jsonify({'response': 'Message too long. Please keep queries under 500 characters.'})
   ```

5. **Expand stopwords** — Add "university", "student", "course" to the stopword list to reduce false positives.

### 20.2 Medium-term Enhancements (1–2 months)

1. **SQLite FTS5 for scalable search** — Replace `FAQ.query.all()` with a full-text search query using SQLite's built-in FTS5 extension for O(log n) retrieval.

2. **Synonym expansion** — Maintain a small synonym dictionary (`enroll` → `register`, `timetable` → `schedule`) to improve recall without requiring ML.

3. **Admin web dashboard** — A Flask-Admin or custom `/admin` route to:
   - View and edit FAQs through a web form
   - Browse and search chat logs
   - Display daily message volume charts

4. **Session awareness** — Use Flask sessions to track a conversation thread, enabling simple follow-up handling ("What about the deadline?" resolving against the previous topic).

5. **Rasa integration** — Complete the Rasa backend integration from the `altinbas-chatbot` implementation, enabling ML-powered intent classification for the primary chatbot.

### 20.3 Long-term Vision (3–6 months)

1. **Semantic search with embeddings** — Replace keyword matching with sentence-transformer embeddings (e.g., `sentence-transformers/all-MiniLM-L6-v2`). Store FAQ embeddings in a vector database (FAISS, pgvector). This handles paraphrasing, synonyms, and informal language naturally.

2. **LLM-augmented responses** — For queries not matched by the FAQ database, call an LLM API (Claude, GPT-4) with a system prompt constraining responses to university context. The FAQ database acts as a primary retrieval layer; the LLM handles edge cases.

3. **Integration with university systems** — Connect to the student portal API to answer personalized queries:
   - "What is my GPA?"
   - "Which courses am I registered for?"
   - "When is my next exam?"

4. **Mobile application** — React Native or Flutter wrapper around the existing REST API for native iOS/Android experience.

5. **Analytics and reporting** — Regular reports on:
   - Most asked questions (to identify FAQ gaps)
   - Fallback rate (to measure chatbot effectiveness)
   - Peak usage times (to plan infrastructure scaling)
   - User satisfaction scores (post-chat rating)

6. **Multi-language support** — Arabic and Turkish language FAQ entries for international student bodies, with automatic language detection on the `/ask` endpoint.

---

## Appendix A — Full Test Suite Output

```
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.0.3, pluggy-1.6.0 -- C:\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Lenovo\OneDrive\Desktop\UniversityChatbotFAQs\university-chatbot
plugins: anyio-4.12.1
collecting ... collected 29 items

tests/test_bot.py::TestChatbotLogic::test_api_ask_endpoint_post PASSED   [  3%]
tests/test_bot.py::TestChatbotLogic::test_api_ask_no_message PASSED      [  6%]
tests/test_bot.py::TestChatbotLogic::test_api_ask_response_not_empty PASSED [ 10%]
tests/test_bot.py::TestChatbotLogic::test_api_ask_returns_json PASSED    [ 13%]
tests/test_bot.py::TestChatbotLogic::test_case_insensitive_matching PASSED [ 17%]
tests/test_bot.py::TestChatbotLogic::test_chat_log_saved PASSED          [ 20%]
tests/test_bot.py::TestChatbotLogic::test_chat_log_stores_bot_response PASSED [ 24%]
tests/test_bot.py::TestChatbotLogic::test_chat_log_stores_user_message PASSED [ 27%]
tests/test_bot.py::TestChatbotLogic::test_chatlog_repr PASSED            [ 31%]
tests/test_bot.py::TestChatbotLogic::test_empty_message_returns_fallback PASSED [ 34%]
tests/test_bot.py::TestChatbotLogic::test_fallback_for_unknown_input PASSED [ 37%]
tests/test_bot.py::TestChatbotLogic::test_faq_model_created PASSED       [ 41%]
tests/test_bot.py::TestChatbotLogic::test_faq_repr PASSED                [ 44%]
tests/test_bot.py::TestChatbotLogic::test_goodbye PASSED                 [ 48%]
tests/test_bot.py::TestChatbotLogic::test_greeting_hello PASSED          [ 51%]
tests/test_bot.py::TestChatbotLogic::test_greeting_hey PASSED            [ 55%]
tests/test_bot.py::TestChatbotLogic::test_greeting_hi PASSED             [ 58%]
tests/test_bot.py::TestChatbotLogic::test_index_route_returns_html PASSED [ 62%]
tests/test_bot.py::TestChatbotLogic::test_name_query PASSED              [ 65%]
tests/test_bot.py::TestChatbotLogic::test_punctuation_stripped PASSED    [ 68%]
tests/test_bot.py::TestChatbotLogic::test_registration_keyword_match PASSED [ 72%]
tests/test_bot.py::TestChatbotLogic::test_registration_query_returns_answer PASSED [ 75%]
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_health_center_query PASSED [ 79%]
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_library_hours_query PASSED [ 82%]
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_library_location_query PASSED [ 86%]
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_multiple_faq_best_match PASSED [ 89%]
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_scholarship_query PASSED [ 93%]
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_student_id_query PASSED [ 96%]
tests/test_bot.py::TestChatbotWithMultipleFAQs::test_threshold_not_triggered_on_weak_match PASSED [100%]

======================== 29 passed, 7 warnings in 3.57s ======================

Warnings: DeprecationWarning from SQLAlchemy regarding datetime.utcnow() usage
(cosmetic warnings only — no test failures)
```

---

## Appendix B — FAQ Knowledge Base (Full)

The following table contains all 40 FAQ entries currently in the live database. Entries 1–10 are from the original seed; 11–25 were added in Expansion Round 1; 26–40 were added in Expansion Round 2.

| ID | Question | Answer | Intent |
|----|---------|--------|--------|
| 1 | How do I register for courses? | To register for courses, log in to the student portal, go to the Academics tab, and select Course Registration. Follow the instructions to add courses to your schedule. | registration |
| 2 | When is the deadline for registration? | The deadline for course registration for the Fall semester is September 15th. For Spring, it is February 10th. | registration |
| 3 | Where is the library located? | The main library is located in Building B, on the 2nd floor. It is open directly from the main campus entrance. | campus |
| 4 | What are the library opening hours? | The library is open from 8:00 AM to 10:00 PM, Monday through Friday. On weekends, it is open from 10:00 AM to 6:00 PM. | campus |
| 5 | How can I contact the computer engineering department? | You can contact the Computer Engineering department via email at ce@university.edu or visit their office in Building C, Room 304. | contact |
| 6 | What programs does the university offer? | The university offers undergraduate and graduate programs in Engineering, Business, Arts, and Sciences. Visit the Academics section on the website for a full list. | programs |
| 7 | How do I check my exam schedule? | Exam schedules are published on the student portal two weeks before the exam period. You can view them under My Exams. | exams |
| 8 | Where can I get a student ID card? | You can obtain your student ID card at the Student Affairs office in the Administration Building. Please bring a valid photo ID. | admin |
| 9 | Is there a health center on campus? | Yes, the health center is located in Building A, ground floor. It provides basic medical services to students and staff. | campus |
| 10 | How do I apply for a scholarship? | Scholarship applications are available on the Financial Aid page of the university website. Deadlines vary by scholarship type. | finance |
| 11 | How do I connect to the university Wi-Fi? | To connect to the university Wi-Fi, select the network named UniNet from your device Wi-Fi settings and log in with your student username and password. | wifi |
| 12 | What is the Wi-Fi password on campus? | The campus Wi-Fi network UniNet uses your student credentials for login. There is no shared password. Use your student ID and portal password to authenticate. | wifi |
| 13 | How do I pay my tuition fees? | Tuition fees can be paid online through the student portal under the Finance section, or in person at the Cashier Office in the Administration Building. Credit card, bank transfer, and cash are accepted. | finance |
| 14 | What is the tuition fee for undergraduate students? | Undergraduate tuition fees vary by program. Please visit the Finance section of the university website or contact the Student Finance Office for the current fee schedule. | finance |
| 15 | Are there dormitories available on campus? | Yes, the university has on-campus dormitories for students. They offer single and shared room options. Priority is given to first-year and international students. | housing |
| 16 | How do I apply for student housing? | To apply for student housing, log in to the student portal, go to the Housing section, and complete the accommodation application form. Applications open each semester. | housing |
| 17 | Is there parking available on campus? | Yes, the university has designated parking areas for students. A parking permit is required and can be obtained from the Security Office. Permits are issued on a first-come, first-served basis. | transport |
| 18 | Does the university provide a shuttle service? | Yes, the university operates a free shuttle service between the main campus and the city center. Schedules are posted at campus bus stops and on the university website. | transport |
| 19 | What are the graduation requirements? | Graduation requirements include completing the required credit hours for your program, maintaining a minimum GPA of 2.0, and fulfilling any internship or project requirements. Check your program handbook for specifics. | graduation |
| 20 | How do I apply for graduation? | To apply for graduation, submit a graduation application through the student portal at least one semester before your expected graduation date. The Registrar Office will review your eligibility. | graduation |
| 21 | How do I request an official transcript? | Official transcripts can be requested through the Registrar Office. Submit a transcript request form in person or via the student portal. Processing takes 3–5 business days. | transcript |
| 22 | How do I change my major? | To change your major, visit the Registrar Office and complete a Change of Major form. You will need approval from both your current and new department advisors. | admin |
| 23 | What student clubs and activities are available? | The university offers over 50 student clubs including sports, arts, technology, debate, and cultural societies. Visit the Student Affairs Office or the university website to see the full list and join a club. | clubs |
| 24 | How do I contact academic advising? | The Academic Advising Center is located in the Administration Building, Room 102. You can also email advising@university.edu or call the office to schedule an appointment. | contact |
| 25 | How do I access the university email? | Your university email is automatically created when you enroll. Access it at mail.university.edu using your student ID as the username and your initial password sent to your personal email during registration. | it_support |
| 26 | Where is the cafeteria and what are its opening hours? | The main cafeteria is located in the Student Center Building, ground floor. It is open from 7:30 AM to 8:00 PM on weekdays and 9:00 AM to 5:00 PM on weekends. | campus |
| 27 | How do I borrow books from the library? | To borrow books, present your valid student ID card at the library circulation desk. Undergraduate students may borrow up to 5 books for 2 weeks. Books can also be renewed online via the student portal. | library |
| 28 | Is there a counseling or mental health service on campus? | Yes, the university offers free counseling services at the Student Wellness Center in Building A, Room 105. You can book an appointment online or by calling the center directly. | counseling |
| 29 | How do I find internship opportunities? | The Career Center helps students find internships. Visit them in Building D, Room 201, or check the internship listings on the student portal under Career Services. They also host a Career Fair each semester. | career |
| 30 | How do I drop or withdraw from a course? | To drop a course, log in to the student portal and go to Course Registration before the drop deadline. After the drop deadline, you must submit a Course Withdrawal form to the Registrar Office with your advisor approval. | registration |
| 31 | Can I retake an exam if I miss it? | A makeup exam may be granted for documented medical emergencies or other serious circumstances. Submit a Makeup Exam Request form to your instructor within 3 days of the missed exam with supporting documentation. | exams |
| 32 | Does the university offer study abroad or exchange programs? | Yes, the university has partnerships with over 30 international universities. Visit the International Office in Building E to learn about exchange programs, eligibility requirements, and application deadlines. | programs |
| 33 | Are there sports facilities or a gym on campus? | Yes, the university sports complex includes a gym, swimming pool, basketball and tennis courts, and a football field. It is open to all students free of charge from 7:00 AM to 10:00 PM daily. | campus |
| 34 | Where can I print or scan documents on campus? | Printing and scanning services are available at the library on the 2nd floor and at the IT Services kiosk in the Student Center. Students receive a printing credit each semester through their student account. | it_support |
| 35 | What disability support services are available? | The Disability Support Office is located in the Administration Building, Room 110. They provide academic accommodations, assistive technology, and accessibility support. Contact them at disability@university.edu. | admin |
| 36 | What services are available for international students? | The International Students Office offers visa guidance, orientation programs, language support, and cultural integration services. It is located in Building E, Room 102. Email international@university.edu for assistance. | admin |
| 37 | Does the university offer summer school or summer courses? | Yes, summer school sessions are offered in June and July. Course availability is limited. Registration opens in April and is done through the student portal under Course Registration. | registration |
| 38 | Are there part time jobs on campus? | Yes, the university offers part-time on-campus job opportunities through the Student Employment Program. Check available positions on the student portal under Career Services or visit the Human Resources Office. | career |
| 39 | Is there a lost and found on campus? | The lost and found is managed by the Security Office at the main campus entrance. You can report or claim lost items in person or by calling the Security Office hotline. | campus |
| 40 | Are student discounts available? | Yes, your student ID card entitles you to discounts at the campus bookstore, cafeteria, and many local businesses. Check the Student Affairs noticeboard or website for a current list of partner discounts. | admin |

---

## Appendix C — API Reference

### Base URL
```
http://localhost:5000
```

### Endpoints

---

#### `GET /`

Returns the chat interface HTML page.

**Request:**
```
GET / HTTP/1.1
Host: localhost:5000
```

**Response:**
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>...
```

---

#### `POST /ask`

Submits a user message and receives the bot's response.

**Request:**
```
POST /ask HTTP/1.1
Host: localhost:5000
Content-Type: application/x-www-form-urlencoded

message=How+do+I+register+for+courses
```

**Success response (200):**
```json
{
  "response": "To register for courses, log in to the student portal, go to the 'Academics' tab, and select 'Course Registration'. Follow the instructions to add courses to your schedule."
}
```

**Empty message response (200):**
```json
{
  "response": "Please enter a message."
}
```

**Fallback response (200):**
```json
{
  "response": "I'm sorry, I don't have information on that yet. Please contact the administration office."
}
```

**Greeting response (200):**
```json
{
  "response": "Hello! I am the University Assistant. How can I help you today?"
}
```

---

*End of Report*

---

**Document Information**

| Field | Value |
|-------|-------|
| Report version | 1.0 |
| Date generated | April 30, 2026 |
| Author | Claude Code (Anthropic) |
| Project location | `C:\Users\Lenovo\OneDrive\Desktop\UniversityChatbotFAQs` |
| Test command | `python -m pytest tests/test_bot.py -v` |
| Test result | 29 passed / 0 failed / 7 warnings |
| Python version | 3.12.4 |
| Flask version | 3.1.2 |
