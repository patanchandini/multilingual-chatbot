# Multilingual Chatbot API



🔗 **Live API URL:** [https://multilingual-chatbot-0hfk.onrender.com](https://multilingual-chatbot-0hfk.onrender.com)

📚 **Interactive Swagger UI (Try it out!):** [https://multilingual-chatbot-0hfk.onrender.com/docs](https://multilingual-chatbot-0hfk.onrender.com/docs)



A complete, production-ready conversational AI backend that supports multiple languages, mixed-language messages, context retention, and strict session management. Built with Python and FastAPI.

## 🚀 Features

This project fulfills all requirements of the specified task:
- **Multi-Language Support:** English, Hindi, Tamil, and Spanish. Detects language dynamically.
- **Mixed-Language & Transliteration:** Understands phrases like "track order 12345 ki stithi" by evaluating script ratios and transliteration dictionaries.
- **Entity Preservation:** Extracts and preserves names, order IDs, dates, and product codes verbatim without translation mangling.
- **Context Retention:** Maintains a 10-turn context window and a rolling summary for longer conversations.
- **Session Isolation:** Simultaneous users (`customer_id`) have completely isolated state and context.
- **Confidence Gating:** If language or intent confidence is low, the bot automatically requests clarification.
- **Correction Handling:** Understands corrections (e.g., "no, I meant 22222") and updates the entity in the session memory.
- **Configurable Expiry:** Sessions expire after 30 minutes of inactivity. If the user returns within 24 hours, the session resumes with its summary intact; otherwise, a new session begins.
- **Spelling & Multiple Requests:** Handles typos, transliterated inputs, and multiple requests in a single sentence.

## 📂 Project Structure

```text
multilingual-chatbot/
├── app.py                  # FastAPI web server wrapper
├── config.yaml             # Configurable thresholds, languages, and timers
├── run_demo.py             # Terminal demonstration script
├── tests/                  # Pytest suite (12 passing tests)
├── src/chatbot/            # Core chatbot logic
│   ├── chatbot.py          # Main orchestrator
│   ├── language_detector.py
│   ├── entity_extractor.py
│   ├── session_manager.py
│   ├── spell_corrector.py
│   └── ...
└── requirements.txt        # Dependencies
🛠️ Installation
Clone the repository:

bash
git clone https://github.com/YOUR_USERNAME/multilingual-chatbot.git
cd multilingual-chatbot
Install the required dependencies:

bash
pip install -r requirements.txt
🏃‍♂️ How to Run
Option 1: The Web API (Recommended)
Start the FastAPI server:

bash
python -m uvicorn app:app --reload --port 8000
Once running, open your browser and go to http://127.0.0.1:8000/docs. This opens the interactive Swagger UI where you can send POST /chat requests and inspect the session state via GET /session/{customer_id}.

Option 2: The Terminal Demo
To see a scripted demonstration of all the features (mixed language, corrections, session expiry, etc.):

bash
python run_demo.py
🧪 Running Tests
The project includes a comprehensive test suite verifying language detection, entity extraction, session expiry logic, and the correction flow.

bash
pytest -q
Expected Output: 12 passed

⚙️ Configuration
All rules are driven by config.yaml. You can adjust:

languages (e.g., add French)

lang_conf_min (Clarification threshold)

idle_timeout_sec (Default: 30 minutes)

resume_window_sec (Default: 24 hours)

🔌 API Endpoints
POST /chat: Send a message. Requires {"customer_id": "string", "text": "string"}.

GET /session/{customer_id}: View the active memory (language, turns, summary, last_activity).

GET /health: Basic API health check.

text

*(Note: Don't forget to replace `YOUR_USERNAME` in the clone URL with your actual GitHub username once you push it!)*

