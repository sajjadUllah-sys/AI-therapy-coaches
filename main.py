import streamlit as st
import os
from dotenv import load_dotenv
from anne import AnneCoach
from lin import LinCoach

load_dotenv()

class CoachingApp:
    def __init__(self):
        self.anne = AnneCoach(api_key=os.getenv('OPENAI_API_KEY'))
        self.lin = LinCoach(api_key=os.getenv('OPENAI_API_KEY'))
    
    def initialize_session(self):
        """Initialize session state variables"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'coach_selected' not in st.session_state:
            st.session_state.coach_selected = None
        if 'conversation_summary' not in st.session_state:
            st.session_state.conversation_summary = ""
    
    def render_coach_selection(self):
        """Render coach selection page"""
        st.title("🧠 AI Coaching Platform")
        st.markdown("### Choose Your Coach")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👩‍⚕️ Dr. Anne Rosental")
            st.markdown("""
            **Former Psychologist & Senior Coach**
            - 35+ years experience
            - Focus: Emotional self-regulation, inner child work
            - Style: Warm, nurturing, reflective
            - Best for: Deep emotional exploration, self-compassion
            """)
            if st.button("Choose Dr. Anne", use_container_width=True):
                st.session_state.coach_selected = 'anne'
                st.rerun()
        
        with col2:
            st.markdown("#### 👨‍💼 Hiro Lin")
            st.markdown("""
            **Business Psychologist & Executive Coach**
            - 20 years experience
            - Focus: Leadership, decision-making, goal clarity
            - Style: Direct, pragmatic, action-oriented
            - Best for: Quick wins, behavioral change, accountability
            """)
            if st.button("Choose Hiro", use_container_width=True):
                st.session_state.coach_selected = 'lin'
                st.rerun()
    
    def render_chat_interface(self):
        """Render main chat interface"""
        coach_name = "Dr. Anne Rosental" if st.session_state.coach_selected == 'anne' else "Hiro Lin"
        coach_obj = self.anne if st.session_state.coach_selected == 'anne' else self.lin
        
        st.title(f"💬 Session with {coach_name}")
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"### Current Coach: {coach_name}")
            if st.button("Switch Coach"):
                st.session_state.coach_selected = None
                st.session_state.messages = []
                st.session_state.conversation_summary = ""
                st.rerun()
            
            if st.button("Clear Chat"):
                st.session_state.messages = []
                st.session_state.conversation_summary = ""
                st.rerun()
            
            st.markdown("---")
            st.markdown("**🛡️ Safety Notice**")
            st.markdown("This is not therapy. In crisis, contact:")
            st.markdown("🇩🇪 Germany: 0800 111 0 111")
            st.markdown("🌍 International: findahelpline.com")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Share what's on your mind..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get coach response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = coach_obj.get_response(
                        user_message=prompt,
                        conversation_history=st.session_state.messages[:-1],
                        conversation_summary=st.session_state.conversation_summary
                    )
                    
                    st.markdown(response['message'])
                    
                    # Check for safety flag
                    if response.get('safety_flag'):
                        st.warning("⚠️ Safety protocol activated. Please seek professional help.")
                    
                    # Update conversation summary periodically
                    if len(st.session_state.messages) % 10 == 0:
                        st.session_state.conversation_summary = coach_obj.summarize_conversation(
                            st.session_state.messages
                        )
            
            st.session_state.messages.append({"role": "assistant", "content": response['message']})
    
    def run(self):
        """Main app runner"""
        st.set_page_config(page_title="AI Coaching", page_icon="🧠", layout="wide")
        self.initialize_session()
        
        if st.session_state.coach_selected is None:
            self.render_coach_selection()
        else:
            self.render_chat_interface()

if __name__ == "__main__":
    app = CoachingApp()
    app.run()