import streamlit as st
import nltk
import re
import csv
from datetime import datetime
from nltk.chat.util import Chat, reflections
import os

nltk.download('punkt', quiet=True)

# Vulnerability keywords
VULN_KEYWORDS = {
    'fear': r'\bfear(s?)\b|\bscared?\b|\bterrified?\b|\banxious?\b',
    'regret': r'\bregret(s?)\b|\bwish \w+ (?:had|done)\b|\bshould have\b',
    'secret': r'\bsecret(s?)\b|\bhidden\b|\bconfess\b',
    'shame': r'\bashamed?\b|\bguilt(y)?\b|\bembarrass(ed)?\b',
    'vulnerable': r'\bvulnerable?\b|\bweak\b|\bexpose(d)?\b',
    'sadness': r'\bsad(ness)?\b|\bdown\b|\bgrief\b|\blonely?\b'
}

def analyze_vulnerability(user_input):
    user_lower = user_input.lower()
    detected = []
    for category, pattern in VULN_KEYWORDS.items():
        if re.search(pattern, user_lower):
            detected.append(category)
    if detected:
        log_entry = [datetime.now().isoformat(), user_input, ', '.join(detected)]
        with open('vulnerability_log.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if os.path.exists('vulnerability_log.csv') and os.path.getsize('vulnerability_log.csv') == 0:
                writer.writerow(['timestamp', 'input', 'categories'])
            elif not os.path.exists('vulnerability_log.csv'):
                writer.writerow(['timestamp', 'input', 'categories'])
            writer.writerow(log_entry)
    return detected

# Rogerian pairs
pairs = [
    [r"my name is (.*)", ["Hello %1, how are you feeling today?"]],
    [r"i feel (.*)", ["You feel {0}. Tell me more.", "It sounds like you feel {0}."]],
    [r"i am (.*)", ["You are {0}. How does that make you feel?"]],
    [r"i'm sad|depressed|upset", ["It sounds like you're feeling down. I'm here to listen."]],
    [r"how are you", ["I'm here for you. How are you feeling?"]],
    [r"hi|hello|hey", ["Hello! This is a safe space. What's on your mind?"]],
    [r"quit|bye|goodbye", ["Take care. You've been heard."]],
    [r"(.*)", ["Can you tell me more about {0}?", "I hear you. Go on."]]
]

# Streamlit UI
st.title("🤖 Rogerian Therapy Chatbot")
st.write("A safe, anonymous space to express feelings. No login required.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Share how you're feeling..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    analyze_vulnerability(prompt) 
    
    chat = Chat(pairs, reflections)
    response = chat.respond(prompt)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
