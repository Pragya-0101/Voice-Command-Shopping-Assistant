import streamlit as st
from streamlit_mic_recorder import speech_to_text
from datetime import datetime
import re

st.set_page_config(page_title="Voice Shopping Assistant", layout="centered")

# ---------- Session State ----------
if "shopping_list" not in st.session_state:
    st.session_state.shopping_list = []
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

# ---------- Data ----------
CATEGORIES = {
    "dairy": ["milk", "cheese", "yogurt", "butter"],
    "produce": ["apple", "banana", "orange", "carrot", "tomato"],
    "snacks": ["chips", "cookies", "popcorn"],
    "beverages": ["juice", "water", "coffee", "tea"],
    "meat": ["chicken", "beef", "fish"],
    "pantry": ["rice", "pasta", "flour", "sugar"]
}

SUBSTITUTES = {
    "milk": ["almond milk", "oat milk"],
    "butter": ["margarine"],
    "coffee": ["tea"]
}

SEASONAL = {
    8: ["ice cream", "watermelon"],
    9: ["apples", "pumpkins"],
    12: ["chocolate", "nuts"]
}

# ---------- Helper Functions ----------
def categorize(item):
    item = item.lower()
    for cat, keywords in CATEGORIES.items():
        if any(k in item for k in keywords):
            return cat
    return "other"

def parse_command(text):
    text = text.lower().strip()
    qty_match = re.search(r'\d+', text)
    qty = int(qty_match.group()) if qty_match else 1
    item = re.sub(r'\d+', '', text)
    item = re.sub(r'(add|buy|get|remove|delete|i need|i want|please)', '', item).strip()
    return item, qty

def add_item(name, qty=1):
    name = name.strip()
    if not name:
        return
    for i in st.session_state.shopping_list:
        if i["name"] == name.lower():
            i["qty"] += qty
            return
    st.session_state.shopping_list.append({
        "name": name.lower(), "qty": qty, "category": categorize(name)
    })

def remove_item(name):
    st.session_state.shopping_list = [
        i for i in st.session_state.shopping_list if i["name"] != name.lower().strip()
    ]

def handle_command(text):
    text = text.lower()
    if "remove" in text or "delete" in text:
        item, _ = parse_command(text)
        remove_item(item)
        st.toast(f"Removed {item}")
    elif "clear" in text:
        st.session_state.shopping_list = []
        st.toast("List cleared")
    else:
        item, qty = parse_command(text)
        add_item(item, qty)
        st.toast(f"Added {qty}x {item}")

# ---------- Voice Input ----------
st.title("🛒 Voice Shopping Assistant")
st.caption("Tap the mic, speak a command, then tap again to stop.")

voice_text = speech_to_text(
    language="en",
    start_prompt="🎤 Start",
    stop_prompt="⏹ Stop",
    just_once=True,
    use_container_width=True,
    key="mic"
)

if voice_text and voice_text != st.session_state.voice_text:
    st.session_state.voice_text = voice_text
    st.write(f"Heard: *{voice_text}*")
    handle_command(voice_text)
    st.rerun()

# ---------- Text fallback (typing works too) ----------
typed = st.text_input("Or type a command", placeholder="Add 2 apples / Remove milk / Clear")
if st.button("Submit"):
    if typed:
        handle_command(typed)

st.markdown("---")

# ---------- Shopping List ----------
st.subheader("📋 Shopping List")
if st.session_state.shopping_list:
    grouped = {}
    for item in st.session_state.shopping_list:
        grouped.setdefault(item["category"], []).append(item)

    for cat, items in grouped.items():
        st.markdown(f"**{cat.title()}**")
        for item in items:
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(item["name"])
            c2.write(f"x{item['qty']}")
            if c3.button("❌", key=f"del_{item['name']}"):
                remove_item(item["name"])
                st.rerun()
else:
    st.info("List is empty. Try the mic or type a command above.")

st.markdown("---")

# ---------- Suggestions ----------
st.subheader("💡 Suggestions")
month = datetime.now().month
seasonal = SEASONAL.get(month, [])
col1, col2 = st.columns(2)

with col1:
    st.caption("Seasonal picks")
    for s in seasonal:
        if st.button(f"+ {s}", key=f"season_{s}"):
            add_item(s)
            st.rerun()

with col2:
    st.caption("Substitutes")
    for item in st.session_state.shopping_list:
        subs = SUBSTITUTES.get(item["name"], [])
        for s in subs:
            if st.button(f"+ {s}", key=f"sub_{s}"):
                add_item(s)
                st.rerun()

st.caption("Tip: click 🎤 and say things like 'add 2 bottles of milk' or 'remove milk'")