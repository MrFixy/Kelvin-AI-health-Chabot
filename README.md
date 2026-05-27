# Kelvin — AI Mental Health Chatbot

Kelvin is an AI-powered mental health chatbot that detects emotion and mental state from user messages and responds with empathy and care. Built with a Flask backend and a clean multi-page frontend.

---

## Features

- Emotion detection (sadness, anger, fear, joy, anxiety, and more)
- Mental state classification (depression, anxiety, stress)
- Empathetic, context-aware responses
- Clean, responsive UI with chat, about, and contact pages
- Always-available — no login required

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Vanilla JS |
| Backend | Python, Flask, Flask-CORS |
| ML | scikit-learn, pickle |
| Email | EmailJS |

---

## Project Structure

```
Kelvin/
├── Pages/
│   ├── index.html          # Landing page
│   ├── chat.html           # Chat interface
│   ├── about.html          # Team & values
│   └── contact.html        # Contact form
├── Scripts/
│   └── app.js              # Shared JS (nav, animations)
├── Style/
│   └── styles.css          # Shared styles
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
└── Models/
    └── Model/
        ├── mental_model.pkl    # Mental state classifier
        ├── emotion_model.pkl   # Emotion classifier
        └── vectorizer.pkl      # Text vectorizer
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MrFixy/Kelvin-AI-health-Chabot.git
cd Kelvin-AI-health-Chabot
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your models

Place your trained model files inside `Models/Model/`:

```
Models/Model/mental_model.pkl
Models/Model/emotion_model.pkl
Models/Model/vectorizer.pkl
```

### 4. Run the backend

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`

### 5. Open the frontend

Open `index.html` in your browser, or serve it with a local server:

```bash
npx serve .
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info |
| GET | `/health` | Backend & model status |
| POST | `/predict` | Predict emotion & mental state |

### `/predict` example

**Request:**
```json
{ "message": "I've been feeling really down lately" }
```

**Response:**
```json
{
  "reply": "That sounds really heavy… I'm here with you.",
  "emotion": "sadness",
  "mental_state": "depression"
}
```

---

## Contact Form Setup (EmailJS)

The contact page uses [EmailJS](https://www.emailjs.com) to send emails without a backend. To configure it:

1. Create a free account at emailjs.com
2. Add an Email Service (Gmail recommended)
3. Create a template using variables: `{{from_name}}`, `{{from_email}}`, `{{subject}}`, `{{message}}`
4. Open `contact.html` and fill in:

```javascript
const EMAILJS_PUBLIC_KEY  = "your_public_key";
const EMAILJS_SERVICE_ID  = "your_service_id";
const EMAILJS_TEMPLATE_ID = "your_template_id";
```

---



---

## Disclaimer

Kelvin is not a substitute for professional mental health care. If you are in crisis, please reach out to a licensed professional or a crisis helpline.

---

## License

© 2025 Kelvin. All rights reserved.
