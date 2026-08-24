# 🛒 Voice Shopping Assistant

A simple voice-controlled shopping list app built with Streamlit.

## Features
- Real voice input (uses your browser's built-in speech recognition — click the mic 🎤)
- Text input also works if you'd rather type
- Auto-categorizes items (dairy, produce, snacks, etc.)
- Quantity detection ("add 2 apples")
- Seasonal suggestions based on current month
- Substitute suggestions (e.g. almond milk for milk)
- Add / remove items

## How to run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## How voice works
Uses the `streamlit-mic-recorder` package, which wraps the browser's
built-in speech recognition (Web Speech API) as a proper two-way
Streamlit component. No API key needed — click Start, speak, click Stop,
and the recognized text is sent straight to Python.

**Note:** Voice recognition needs Chrome or Edge, and the site must be
opened over HTTPS (Streamlit Cloud gives you HTTPS automatically).

## Deployment
Deployed on Streamlit Cloud: [add your live link here]

## Tech Stack
- Streamlit (UI + app logic)
- Browser Web Speech API (voice recognition)
- Plain Python (regex-based command parsing, no heavy NLP library needed)