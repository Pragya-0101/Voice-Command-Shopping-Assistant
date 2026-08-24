# Approach

## Problem
Build a voice-controlled shopping list app with smart suggestions in a
limited time frame.

## Solution
I built the app in Streamlit for fast development and easy deployment.
For voice input, I used the browser's built-in Web Speech API instead of
a paid cloud service — it runs entirely client-side, needs no API key,
and works well in Chrome/Edge. The recognized text is sent back to the
Streamlit app and parsed with simple regex to pull out the item name and
quantity (e.g. "add 2 apples" → item: apples, qty: 2).

## Key Decisions
- **Voice**: Web Speech API (free, no backend, no setup)
- **NLP**: Kept it lightweight — regex-based parsing instead of a full
  NLP library, since commands follow predictable patterns
- **Categorization**: Rule-based keyword matching (fast, no ML needed)
- **Storage**: Session state (resets per session — fine for a demo)
- **Fallback**: Added a text input so the app still works if voice isn't
  supported or the mic isn't available

## Future Improvements
- Persistent storage (database instead of session state)
- Multilingual voice support
- ML-based personalized recommendations from purchase history