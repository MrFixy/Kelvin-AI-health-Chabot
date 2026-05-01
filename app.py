import os
import pickle
# joblib
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── SETUP ────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ── LOAD MODELS ──────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'Models')

def load_model(filename):
    path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Not found: {path}")
    with open(path, 'rb') as f:
        return pickle.load(f)

try:
    mental_model  = load_model('Model/mental_model.pkl')
    emotion_model = load_model('Model/emotion_model.pkl')
    vectorizer    = load_model('Model/vectorizer.pkl')
    MODELS_READY  = True
    logger.info("✅ All models loaded.")
except FileNotFoundError as e:
    MODELS_READY = False
    logger.error(f"❌ {e}")
    logger.error("Place mental_model.pkl, emotion_model.pkl, vectorizer.pkl inside a Models/ folder.")

# ── RESPONSE TEMPLATES ───────────────────────────────────────
REPLIES = {
    "sadness":  "That sounds really heavy… I'm here with you. Would you like to share more about what's been going on?",
    "anger":    "I can feel the frustration in what you're sharing. What do you think has been building up the most?",
    "fear":     "That sounds genuinely stressful. What part of this feels most overwhelming right now?",
    "joy":      "It's really nice to hear something positive 😊 What's been going well for you?",
    "anxiety":  "Anxiety can feel so consuming. Let's slow down — what's been weighing on you the most?",
    "disgust":  "That sounds really unpleasant to deal with. What happened?",
    "surprise": "Sounds like something unexpected came up. How are you feeling about it?",
    "neutral":  "I'm here with you. Tell me a bit more — I'm listening.",
}

MENTAL_ADDONS = {
    "depression": "It sounds like things feel particularly heavy right now. You don't have to carry this alone.",
    "anxiety":    "Anxiety can be exhausting. We can take this one step at a time.",
    "stress":     "A lot seems to be piling up. Let's try to untangle it together.",
}

def generate_reply(emotion: str, mental_state: str) -> str:
    base = REPLIES.get(emotion.lower(), REPLIES["neutral"])
    addon = MENTAL_ADDONS.get(mental_state.lower(), "")
    return f"{base}\n\n{addon}".strip() if addon else base

# ── ROUTES ───────────────────────────────────────────────────
@app.route('/')
def home():
    return jsonify({"service": "Kelvin", "models_ready": MODELS_READY})

@app.route('/health')
def health():
    """Frontend pings this on load to check if backend is up."""
    return jsonify({"ok": MODELS_READY}), (200 if MODELS_READY else 503)

@app.route('/predict', methods=['POST'])
def predict():
    if not MODELS_READY:
        return jsonify({"error": "Models not loaded. Check server logs."}), 503

    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Send JSON with a 'message' field."}), 400

    text = data['message'].strip()
    if not text:
        return jsonify({"error": "Message is empty."}), 400
    if len(text) > 2000:
        return jsonify({"error": "Message too long (max 2000 chars)."}), 400

    try:
        vec          = vectorizer.transform([text])
        emotion_pred = str(emotion_model.predict(vec)[0])
        mental_pred  = str(mental_model.predict(vec)[0])
        reply        = generate_reply(emotion_pred, mental_pred)

        logger.info(f"emotion={emotion_pred} | mental={mental_pred} | '{text[:60]}'")

        return jsonify({
            "reply":        reply,
            "emotion":      emotion_pred,
            "mental_state": mental_pred,
        })

    except Exception as e:
        logger.exception("Prediction failed")
        return jsonify({"error": "Prediction failed. Check server logs."}), 500

# ── RUN ──────────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"🚀 Starting Kelvin on http://127.0.0.1:{port}")
    app.run(debug=True, port=port)
