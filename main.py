"""
AI Coaching System - Streamlit Frontend
Multi-coach platform with Dr. Anne Rosental and Hiro Lin
"""

import streamlit as st
from anne_rosental_coach import create_anne_coach
from hiro_lin_coach import create_hiro_coach

# Page configuration
st.set_page_config(
    page_title="AI Coaching Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .coach-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    .coach-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
    }
    .coach-description {
        font-size: 0.95rem;
        color: #555;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #0078d4;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #000000;
        margin-right: 20%;
    }
    .safety-warning {
        background-color: #C43434;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .safety-critical {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'coach_selected' not in st.session_state:
    st.session_state.coach_selected = None
if 'coach_instance' not in st.session_state:
    st.session_state.coach_instance = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'country_code' not in st.session_state:
    st.session_state.country_code = "US"


def reset_session():
    """Reset the coaching session"""
    st.session_state.messages = []
    if st.session_state.coach_instance:
        st.session_state.coach_instance.reset_session()


def select_coach(coach_name, country_code):
    """Select a coach and initialize"""
    reset_session()
    st.session_state.coach_selected = coach_name
    st.session_state.country_code = country_code
    
    # Create coach instance
    if coach_name == "Dr. Anne Rosental":
        st.session_state.coach_instance = create_anne_coach(country_code)
    elif coach_name == "Hiro Lin":
        st.session_state.coach_instance = create_hiro_coach(country_code)
    
    # Get welcome message
    welcome_msg = st.session_state.coach_instance.get_welcome_message()
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})


# Sidebar for coach selection
with st.sidebar:
    st.markdown("### 🧠 AI Coaching Platform")
    st.markdown("---")
    
    # Country selection for helplines
    st.markdown("#### Your Location")
    country_code = st.selectbox(
        "Select your country (for helplines)",
        options=["US", "GB", "DE", "BD"],
        format_func=lambda x: {
            "US": "🇺🇸 United States",
            "GB": "🇬🇧 United Kingdom", 
            "DE": "🇩🇪 Germany",
            "BD": "🇧🇩 Bangladesh"
        }[x],
        index=0
    )
    
    st.markdown("---")
    st.markdown("#### Choose Your Coach")
    
    # Dr. Anne Rosental Card
    with st.container():
        st.markdown("""
        <div class="coach-card">
            <div class="coach-name">👵 Dr. Anne Rosental</div>
            <div class="coach-description">
                <strong>Senior Psychologist & Coach</strong><br>
                35+ years experience<br><br>
                <strong>Specializes in:</strong><br>
                • Emotional self-regulation<br>
                • Inner child work<br>
                • Self-compassion<br>
                • Value-based development<br><br>
                <strong>Style:</strong> Warm, nurturing, emotionally attuned.<br>
                Creates safe space for deep exploration.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Select Dr. Anne Rosental", use_container_width=True):
            select_coach("Dr. Anne Rosental", country_code)
            st.rerun()
    
    st.markdown("---")
    
    # Hiro Lin Card
    with st.container():
        st.markdown("""
        <div class="coach-card">
            <div class="coach-name">🎯 Hiro Lin</div>
            <div class="coach-description">
                <strong>Executive & Behavioral Coach</strong><br>
                20 years experience<br><br>
                <strong>Specializes in:</strong><br>
                • Action-oriented transformation<br>
                • Decision-making<br>
                • Goal clarity<br>
                • Habit formation<br><br>
                <strong>Style:</strong> Direct, focused, results-driven.<br>
                Pragmatic solutions with clear next steps.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Select Hiro Lin", use_container_width=True):
            select_coach("Hiro Lin", country_code)
            st.rerun()
    
    st.markdown("---")
    
    # Session controls
    if st.session_state.coach_selected:
        st.markdown(f"**Current Coach:** {st.session_state.coach_selected}")
        if st.button("🔄 Start New Session", use_container_width=True):
            reset_session()
            st.rerun()
        
        if st.button("🔙 Change Coach", use_container_width=True):
            st.session_state.coach_selected = None
            st.session_state.coach_instance = None
            reset_session()
            st.rerun()


# Main chat interface
if st.session_state.coach_selected is None:
    # Welcome screen when no coach selected
    st.markdown('<h1 class="main-header">Welcome to AI Coaching Platform</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Choose Your Coaching Journey
    
    Select a coach from the sidebar to begin your session. Each coach brings a unique approach:
    
    **Dr. Anne Rosental** offers deep emotional exploration and compassionate guidance. Perfect for:
    - Processing emotions and developing self-compassion
    - Inner child work and healing past wounds
    - Finding clarity through gentle self-discovery
    - Building emotional awareness and regulation
    
    **Hiro Lin** provides action-oriented coaching with clear strategies. Perfect for:
    - Breaking through procrastination and overwhelm
    - Making difficult decisions with confidence
    - Building better habits and achieving goals
    - Reframing limiting beliefs into action
    
    ---
    
    ⚠️ **Important**: This is a coaching tool, not therapy or crisis intervention. If you're experiencing a mental health crisis, please contact emergency services or a crisis helpline immediately.
    """)
    
else:
    # Chat interface when coach is selected
    st.markdown(f'<h1 class="main-header">Coaching Session with {st.session_state.coach_selected}</h1>', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong><br>{message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            coach_name = st.session_state.coach_selected.split()[1]  # Get first name
            
            # Check for safety keywords in response
            is_crisis = any(keyword in message["content"].lower() for keyword in 
                          ["emergency", "crisis", "suicide", "professional help immediately"])
            is_warning = any(keyword in message["content"].lower() for keyword in 
                           ["professional care", "therapist", "counselor", "helpline"])
            
            if is_crisis:
                st.markdown(f"""
                <div class="safety-critical">
                    <strong>🚨 {coach_name}:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            elif is_warning:
                st.markdown(f"""
                <div class="safety-warning">
                    <strong>⚠️ {coach_name}:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>{coach_name}:</strong><br>{message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Share what's on your mind...")
    
    if user_input:
        # Check if session is blocked
        if st.session_state.coach_instance.session_blocked:
            st.error("⛔ This session has been ended for your safety. Please reach out to the professional resources shared above.")
        else:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Generate coach response
            with st.spinner(f"{st.session_state.coach_selected} is thinking..."):
                response = st.session_state.coach_instance.generate_response(user_input)
            
            # Add coach response
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Rerun to display new messages
            st.rerun()


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85rem;'>
    <strong>Disclaimer:</strong> This AI coaching platform is for personal development and support only. 
    It is not a substitute for professional mental health care, medical advice, or emergency services.
    If you're in crisis, please contact emergency services or a crisis helpline immediately.
</div>
""", unsafe_allow_html=True)