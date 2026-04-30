# University FAQ Chatbot

A web-based student assistant chatbot that answers frequently asked questions about university services. Built with Python/Flask and a keyword-matching engine backed by SQLite.

---

## Features

- Instant answers to 40+ student FAQ topics (registration, library, exams, housing, Wi-Fi, and more)
- Modern glassmorphism chat interface
- Typing indicator and smooth message animations
- All conversations logged to a local database
- CLI tool to add new Q&A pairs without touching code

---

## Requirements

- Python 3.10 or higher
- pip

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/YaserAlAji/UniversityChatbotFAQS.git
cd UniversityChatbotFAQS
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
cd university-chatbot
pip install -r requirements.txt
```

**4–5. Initialize & seed the database** *(one-time setup commands included in the file)*

---

## Running the Chatbot

```bash
python run.py
```
Then open **http://localhost:5000**

---

## Running Tests

```bash
python -m pytest tests/test_bot.py -v
```
Expected: **29 passed**
The README also includes a full example questions table, training mode instructions, project structure tree, and tech stack summary.

Want me to change anything (wording, add/remove sections, different format)
