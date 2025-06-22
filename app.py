import streamlit as st
from chatbot3 import ISLChatbot
import pandas as pd

st.set_page_config(
    page_title="ISL Assistant - Non-Manual Features",
    page_icon="👐",
    layout="wide",
)

st.markdown("""
<style>
    .main {
        background-color: #f5f7ff;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #e6f3ff;
    }
    .chat-message.bot {
        background-color: #f0f0f0;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex: 1;
    }
    .sidebar .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 5px solid #4287f5;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .video-container {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

if 'chatbot' not in st.session_state:
    # Initialize chatbot with the ISL data
    st.session_state.chatbot = ISLChatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'search_results' not in st.session_state:
    st.session_state.search_results = []

if 'nmf_results' not in st.session_state:
    st.session_state.nmf_results = []


def display_chat_message(message, is_user=False):
    avatar = "👤" if is_user else "🤖"
    message_class = "user" if is_user else "bot"
    
    st.markdown(f"""
    <div class="chat-message {message_class}">
        <div class="avatar">{avatar}</div>
        <div class="message">{message}</div>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("ISL Assistant")
    st.markdown("### About Indian Sign Language")
    
    with st.expander("What are Non-Manual Features?"):
        st.markdown("""
        Non-Manual Features (NMFs) are crucial components of Indian Sign Language that include:
        - Facial expressions
        - Head movements
        - Eye gaze
        - Body posture
        
        These features modify and enhance the meaning of manual signs, allowing for nuanced communication.
        """)
    
    with st.expander("How to Use This App"):
        st.markdown("""
        1. **Chat**: Ask questions about ISL and NMFs in the main chat area
        2. **Search**: Find specific signs and their variations
        3. **NMF Explorer**: Discover which NMF combinations create specific meanings
        4. **Video Links**: View example videos for specific signs
        """)
    

    st.header("Sign Search")
    search_query = st.text_input("Search for a sign:", key="search_input")
    if st.button("Search"):
        st.session_state.search_results = st.session_state.chatbot.search_signs(search_query)
    

    if st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results)} results")
        for result in st.session_state.search_results:
            if "sign" in result:
                # Display manual sign results
                with st.expander(f"Sign: {result['sign']}"):
                    for ex in result.get('examples', []):
                        st.markdown(f"**With {ex.get('NMF', 'No NMF')}:**")
                        st.markdown(f"Translation: *{ex.get('translation', 'No translation')}*")
                        if 'explanation' in ex:
                            st.markdown(f"Explanation: {ex['explanation']}")
            else:
                # Display YouTube link results
                with st.expander(f"Word: {result.get('Word', 'Unknown')}"):
                    st.markdown(f"**NMF:** {result.get('Non-manual feature', 'Unknown')}")
                    video_link = result.get('Youtube Link', '')
                    if video_link:
                        st.markdown(f"[Watch Video]({video_link})")

    # NMF Explorer
    st.header("NMF Explorer")
    nmf_query = st.text_input("Search for a NMF expression:", key="nmf_input")
    if st.button("Explore NMFs"):
        st.session_state.nmf_results = st.session_state.chatbot.get_nmf_combinations(nmf_query)
    
    # Display NMF results
    if st.session_state.nmf_results:
        st.subheader(f"Found {len(st.session_state.nmf_results)} NMF combinations")
        for result in st.session_state.nmf_results:
            st.markdown(f"**{result.get('Action Combination', 'Unknown')}**")
            st.markdown(f"Meaning: *{result.get('Description', 'No description')}*")

# Main content area
st.title("Indian Sign Language Assistant")
st.markdown("### Focus on Non-Manual Features (NMFs)")


st.markdown("""
<div class="info-box">
    Ask questions about Indian Sign Language, especially about non-manual features like facial expressions, 
    head movements, eye gaze, and body posture. You can also search for specific signs or NMF combinations using 
    the sidebar tools.
</div>
""", unsafe_allow_html=True)

# Display chat messages from history
for message in st.session_state.messages:
    display_chat_message(message["content"], message["role"] == "user")

# Chat input
user_input = st.chat_input("Ask about Indian Sign Language and Non-Manual Features...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    display_chat_message(user_input, is_user=True)
    
    # Get chatbot response
    response = st.session_state.chatbot.chat(user_input)
    
    # Add chatbot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    display_chat_message(response)
    
    # Check if the user is asking about a specific sign to show video
    words = user_input.lower().split()
    for word in words:
        video_link = st.session_state.chatbot.get_youtube_link(word)
        if video_link:
            st.markdown(f"""
            <div class="video-container">
                <h3>Video Example for "{word}"</h3>
                <a href="{video_link}" target="_blank">Watch on YouTube</a>
            </div>
            """, unsafe_allow_html=True)
            break

# Footer
st.markdown("---")
st.markdown("ISL Assistant - Helping you understand Indian Sign Language and Non-Manual Features")