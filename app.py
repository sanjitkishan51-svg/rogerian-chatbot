import nltk
from nltk.chat.util import Chat, reflections

# Download required NLTK data (run once)
nltk.download('punkt')

# Rogerian-style pairs: patterns and reflective responses
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

# Reflections for pronoun swapping (standard NLTK)
print("Rogerian Chatbot (type 'quit' to exit)")
chat = Chat(pairs, reflections)
chat.converse()
