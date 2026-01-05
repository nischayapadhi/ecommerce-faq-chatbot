import streamlit as st
import os
import sys

# --- 1. CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="E-Commerce AI Support",
    page_icon="🤖",
    layout="centered"
)

# --- 2. SETUP PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'Ecommerce_FAQ_Chatbot_dataset_augmented.json')
GLOVE_PATH = os.path.join(BASE_DIR, 'models', 'glove', 'glove.6B.100d.txt')

sys.path.append(SRC_DIR)

# --- 3. IMPORTS ---
try:
    from embeddings import EmbeddingEngine
    from chatbot import SimpleChatbot
    from download_model import check_and_download_model # <--- NEW IMPORT
except Exception as e:
    st.error(f"❌ Critical Import Error: {e}")
    st.stop()

# --- 4. THE OPTIMIZED LOADER (MEMORY CACHE) ---
@st.cache_resource
def load_cached_bot():
    # 1. AUTOMATIC DOWNLOAD TRIGGER
    if not os.path.exists(GLOVE_PATH):
        # Show a spinner because this takes 2-3 minutes
        with st.spinner("📥 Downloading AI Model ..."):
            check_and_download_model()
    
    # 2. Check Data
    if not os.path.exists(DATA_PATH):
        return None, f"Data file not found at: {DATA_PATH}"

    # 3. Load Engine & Bot
    try:
        engine = EmbeddingEngine(GLOVE_PATH)
        engine.load_model()
        bot = SimpleChatbot(DATA_PATH, engine)
        return bot, None
    except Exception as e:
        return None, str(e)

# --- 5. UI LAYOUT ---

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Support Assistant")
    st.markdown("---")
    st.markdown("""
    **✅ I can help with:**
    - Order Tracking
    - Returns & Refunds
    - Shipping Info
    - Payment Methods
    """)
    st.markdown("---")
    st.caption("Powered by GloVe Embeddings")

# Main Page
st.title("💬 E-Commerce Support Chat")
st.markdown("Ask me about your order, shipping, or returns!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your automated support agent. How can I assist you with your order today?"}
    ]

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If this message has debug info stored, show it (optional)
        if "debug_score" in message:
            with st.expander("🔍 Model Logic (History)"):
                st.write(f"Confidence: `{message['debug_score']:.2f}`")
                st.write(f"Matched: `{message['debug_match']}`")

# Load the Bot
if "bot_loaded" not in st.session_state:
    with st.spinner("Initializing AI Brain..."):
        bot_instance, error_msg = load_cached_bot()
        if bot_instance:
            st.session_state.bot = bot_instance
            st.session_state.bot_loaded = True
        else:
            st.error(f"Failed to load bot: {error_msg}")
            st.stop()

# Handle User Input
if prompt := st.chat_input("Type your question here..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate Response
    response_data = st.session_state.bot.get_response(prompt, threshold=0.35)
    
    answer = response_data['answer']
    score = response_data['score']
    matched_q = response_data['matched_question']
    
    # 3. Soft Failure Handling
    if 0.35 < score < 0.55:
        answer = f"I'm not 100% certain, but this seems relevant:\n\n{answer}\n\n*(Confidence: Low)*"
    
    if "I'm sorry" in answer:
        answer += "\n\n**Here are some things I can help with:**\n" \
                  "- 'Where is my order?'\n" \
                  "- 'I want to return an item'\n" \
                  "- 'Do you ship to Canada?'"

    # 4. Save Message with Debug Data
    msg_data = {
        "role": "assistant", 
        "content": answer, 
        "debug_score": score, 
        "debug_match": matched_q
    }
    st.session_state.messages.append(msg_data)

    # 5. Assistant Message Display
    with st.chat_message("assistant"):
        st.markdown(answer)
        
        # --- THE DEBUG INFO BLOCK ---
        with st.expander("🔍 Debug: Why did the AI say this?"):
            st.markdown(f"**Confidence Score:** `{score:.4f}`")
            st.markdown(f"**Internal Match:** *\"{matched_q}\"*")
            
            # Visual Indicator
            if score > 0.8:
                st.success("High Confidence Match (Strong Semantics)")
            elif score > 0.5:
                st.warning("Medium Confidence Match")
            else:
                st.error("Low Confidence (Guessing)")