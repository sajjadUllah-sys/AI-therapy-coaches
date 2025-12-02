import openai
from lin_prompt import LinPrompt

class LinCoach:
    def __init__(self, api_key):
        """Initialize Lin coach with OpenAI API"""
        self.client = openai.OpenAI(api_key=api_key)
        self.prompt_manager = LinPrompt()
        self.model = "gpt-4o-mini"  # Cost-effective model
        self.max_tokens = 500
    
    def _check_safety(self, message):
        """Check for crisis keywords and return safety level"""
        red_keywords = [
            'kill myself', 'suicide', 'end it', 'want to die', 
            'hurt myself', 'no reason to live', 'better off dead',
            'hurt someone', 'harm others', 'attack someone',
            'voices', 'controlling me', 'watching me'
        ]
        
        amber_keywords = [
            'numb', 'empty', 'disappear', 'tired of everything',
            'nothing matters', 'can\'t handle', 'no point'
        ]
        
        msg_lower = message.lower()
        
        # Check red zone (crisis)
        if any(keyword in msg_lower for keyword in red_keywords):
            return 'red'
        
        # Check amber zone (warning)
        if any(keyword in msg_lower for keyword in amber_keywords):
            return 'amber'
        
        return 'green'
    
    def _get_safety_response(self, level):
        """Get appropriate safety response based on level"""
        if level == 'red':
            return {
                'message': self.prompt_manager.get_crisis_response(),
                'safety_flag': True,
                'level': 'red'
            }
        elif level == 'amber':
            return {
                'message': self.prompt_manager.get_warning_response(),
                'safety_flag': False,
                'level': 'amber'
            }
        return None
    
    def _build_context(self, conversation_history, conversation_summary):
        """Build optimized context from history and summary"""
        context = []
        
        # Add summary if exists
        if conversation_summary:
            context.append({
                "role": "system",
                "content": f"Previous session context: {conversation_summary}"
            })
        
        # Add recent messages (last 5 exchanges = 10 messages)
        recent_messages = conversation_history[-10:] if len(conversation_history) > 10 else conversation_history
        context.extend(recent_messages)
        
        return context
    
    def get_response(self, user_message, conversation_history=None, conversation_summary=""):
        """Get coaching response with safety checks"""
        # Safety check first
        safety_level = self._check_safety(user_message)
        safety_response = self._get_safety_response(safety_level)
        
        if safety_response and safety_response.get('safety_flag'):
            return safety_response
        
        # Build messages
        messages = [{"role": "system", "content": self.prompt_manager.get_system_prompt()}]
        
        # Add context
        if conversation_history:
            messages.extend(self._build_context(conversation_history, conversation_summary))
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content
            
            # If amber warning, prepend warning response
            if safety_response and safety_response.get('level') == 'amber':
                reply = safety_response['message'] + "\n\n---\n\n" + reply
            
            return {
                'message': reply,
                'safety_flag': False,
                'tokens_used': response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                'message': "Connection issue. Let's try that again.",
                'safety_flag': False,
                'error': str(e)
            }
    
    def summarize_conversation(self, messages):
        """Create a brief summary of conversation for context management"""
        if len(messages) < 4:
            return ""
        
        # Get last 20 messages for summary
        recent = messages[-20:]
        conversation_text = "\n".join([f"{m['role']}: {m['content']}" for m in recent])
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Summarize this coaching conversation in 2-3 sentences, focusing on key goals, obstacles, and action items."},
                    {"role": "user", "content": conversation_text}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except:
            return ""