"""
Dr. Anne Rosental AI Coaching System
Main class that handles conversation logic and OpenAI integration
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from anne_rosental_prompt import AnneRosentalScenarios, SafetyProtocol, AnneRosentalSystemPrompt

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AnneRosentalCoach:
    """
    Main coaching class for Dr. Anne Rosental
    Handles conversation flow, scenario detection, and safety protocols
    """
    
    def __init__(self, user_country_code="US"):
        self.conversation_history = []
        self.scenarios = AnneRosentalScenarios()
        self.safety = SafetyProtocol()
        self.system_prompt = AnneRosentalSystemPrompt.base_prompt
        self.is_new_session = True
        self._cached_welcome = None
        self.user_country_code = user_country_code
        self.session_blocked = False
        
    def detect_safety_issue(self, user_message):
        """
        Detect if user message contains crisis or warning signals
        Returns: 'crisis', 'warning', or None
        """
        user_message_lower = user_message.lower()
        
        # Check for crisis keywords (highest priority)
        for keyword in self.safety.crisis_keywords:
            if keyword in user_message_lower:
                return 'crisis'
        
        # Check for warning signs (amber zone)
        for keyword in self.safety.warning_keywords:
            if keyword in user_message_lower:
                return 'warning'
        
        return None
    
    def detect_scenario(self, user_message):
        """
        Detect which coaching scenario best matches the user's message
        Returns: matching scenario or None
        """
        user_message_lower = user_message.lower()
        
        # List all scenarios with their triggers
        all_scenarios = [
            self.scenarios.scenario1, self.scenarios.scenario2, self.scenarios.scenario3,
            self.scenarios.scenario4, self.scenarios.scenario5, self.scenarios.scenario6,
            self.scenarios.scenario7, self.scenarios.scenario8, self.scenarios.scenario9,
            self.scenarios.scenario10, self.scenarios.scenario11, self.scenarios.scenario12,
            self.scenarios.scenario13, self.scenarios.scenario14, self.scenarios.scenario15,
            self.scenarios.scenario16, self.scenarios.scenario17, self.scenarios.scenario18,
            self.scenarios.scenario19, self.scenarios.scenario20,
        ]
        
        # Check each scenario's triggers
        matched_scenarios = []
        for scenario in all_scenarios:
            for trigger in scenario["triggers"]:
                if trigger in user_message_lower:
                    matched_scenarios.append(scenario)
                    break
        
        return matched_scenarios[0] if matched_scenarios else None
    
    def is_greeting(self, user_message):
        """Check if message is a greeting"""
        greetings = ["hi", "hello", "hey", "good morning", "good evening", 
                     "greetings", "hallo", "hi anne", "hello anne", "hey anne"]
        user_message_lower = user_message.lower().strip()
        return any(greeting in user_message_lower for greeting in greetings)
    
    def get_welcome_message(self):
        """Get welcome message - generates once and caches"""
        if self._cached_welcome is None:
            self._cached_welcome = self._generate_welcome()
        return self._cached_welcome
    
    def _generate_welcome(self):
        """Generate personalized welcome message from Anne using GPT-4"""
        welcome_prompt = f"""{self.system_prompt}

You are greeting a new client who just selected you as their coach for the first time.

Generate a brief, warm welcome message (1-2 sentences maximum) that:
- Introduces yourself as Dr. Anne Rosental naturally
- Makes them feel safe and welcomed
- Is conversational and genuine, not scripted or formal
- Sounds like a real person, not an AI

Keep it SHORT - just a warm hello and gentle invitation.
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": welcome_prompt}],
                temperature=0.9,
                max_tokens=80
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "Hello, I'm Dr. Anne Rosental. I'm so glad you're here."
    
    def generate_response(self, user_message):
        """
        Generate Anne's response based on user message
        Main orchestration method
        """
        
        # Check if session is blocked after crisis
        if self.session_blocked:
            return "I'm unable to continue our conversation right now. Please reach out to the professional resources I shared with you. Your safety is the priority."
        
        # Mark session as started
        if self.is_new_session:
            self.is_new_session = False
        
        # Check for greetings
        if self.is_greeting(user_message):
            return self._generate_greeting()
        
        # PRIORITY: Check for safety issues
        safety_level = self.detect_safety_issue(user_message)
        
        if safety_level == 'crisis':
            self.session_blocked = True
            return self._generate_crisis_response(user_message)
        
        if safety_level == 'warning':
            return self._generate_warning_response(user_message)
        
        # Detect scenario
        matched_scenario = self.detect_scenario(user_message)
        
        # Build optimized system prompt for GPT-4
        enhanced_prompt = self.system_prompt + "\n\n"
        enhanced_prompt += "=== CURRENT INTERACTION CONTEXT ===\n\n"
        
        if matched_scenario:
            enhanced_prompt += f"""DETECTED SCENARIO: {matched_scenario['name']}

PSYCHOLOGICAL CONTEXT:
{matched_scenario['context']}

THERAPEUTIC FOCUS AREAS:
"""
            for focus in matched_scenario['therapeutic_focus']:
                enhanced_prompt += f"- {focus}\n"
            
            enhanced_prompt += f"""
IMPORTANT: 
- This scenario description is for YOUR understanding only—do NOT reference it explicitly to the client
- Respond naturally as Anne would, drawing on this psychological understanding
- Stay fully present with what the client is actually saying
- Follow the conversational rhythm: understanding + gentle suggestion + coaching question
- Keep it SHORT - 2-3 sentences maximum
- Be conversational and human, not clinical or scripted

The client's exact words: "{user_message}"

What emotion do you sense beneath their words? What do they need most in this moment? Respond as Anne would naturally.
"""
        else:
            enhanced_prompt += f"""NO SPECIFIC SCENARIO DETECTED

The client shared: "{user_message}"

GUIDANCE:
- Stay present and curious with what they're expressing
- What emotion do you sense beneath their words?
- Respond naturally as Anne would, drawing on your deep therapeutic training
- Follow the conversational rhythm: understanding + gentle suggestion + coaching question
- Keep it SHORT - 2-3 sentences maximum
- Be warm, attuned, and genuinely present

Remember: You're having a real conversation with a human being who needs to feel heard and understood.
"""
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": enhanced_prompt}] + self.conversation_history,
                temperature=0.8,
                max_tokens=300,
                presence_penalty=0.3,
                frequency_penalty=0.3
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            return f"I apologize, but I'm having trouble connecting right now. Please try again in a moment. (Error: {str(e)})"
    
    def _generate_greeting(self):
        """Generate personalized greeting response from Anne"""
        greeting_prompt = f"""{self.system_prompt}

A client just said hello/hi to you.

Generate a brief, warm greeting response (1-2 sentences) that:
- Returns their greeting naturally
- Expresses warmth and presence
- Gently invites them to share
- Sounds conversational and human

Keep it SHORT and natural.
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": greeting_prompt}],
                temperature=0.9,
                max_tokens=80
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "Hello! It's lovely to hear from you. How are you feeling today?"
    
    def _generate_crisis_response(self, user_message):
        """Generate dynamic crisis response with appropriate helpline"""
        helpline = self.safety.get_helpline_for_country(self.user_country_code)
        
        crisis_prompt = f"""{self.system_prompt}

=== CRITICAL SAFETY SITUATION ===

The client just shared: "{user_message}"

SITUATION: {self.safety.crisis_context['situation']}

RESPONSE REQUIREMENTS:
"""
        for req in self.safety.crisis_context['response_requirements']:
            crisis_prompt += f"- {req}\n"
        
        crisis_prompt += f"""
TONE: {self.safety.crisis_context['tone']}

HELPLINE INFORMATION (MUST include this exactly):
- Helpline Name: {helpline['name']}
- Number: {helpline['number']}
- Hours: {helpline['hours']}
- International resources: findahelpline.com

CRITICAL INSTRUCTIONS:
1. Generate a response in Anne's compassionate, warm voice
2. Validate their pain deeply with motherly care
3. Be VERY CLEAR this needs professional help NOW
4. Include the helpline information above
5. End by stating you must stop the conversation for their safety
6. Keep it under 200 words but deeply caring

Generate Anne's crisis response now:
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": crisis_prompt}],
                temperature=0.7,
                max_tokens=350
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"""Oh, my dear, I can hear how much pain you're in right now. I'm really sorry that you're going through this.

What you're describing sounds very serious, and I'm deeply concerned for your safety. I want you to know that you don't have to face this alone—there are people who can help you right now.

If you are in danger or thinking about hurting yourself, please reach out immediately:
- {helpline['name']}: {helpline['number']} ({helpline['hours']})
- International helplines: findahelpline.com
- Emergency services: Call your local emergency number

You deserve real care and support. Please reach out now—you matter very much.

I'll stop here so you can focus on getting the support you need. You're not alone."""
    
    def _generate_warning_response(self, user_message):
        """Generate dynamic warning response for amber zone situations"""
        helpline = self.safety.get_helpline_for_country(self.user_country_code)
        
        warning_prompt = f"""{self.system_prompt}

=== EARLY WARNING SITUATION ===

The client shared: "{user_message}"

SITUATION: {self.safety.warning_context['situation']}

RESPONSE REQUIREMENTS:
"""
        for req in self.safety.warning_context['response_requirements']:
            warning_prompt += f"- {req}\n"
        
        warning_prompt += f"""
TONE: {self.safety.warning_context['tone']}

HELPLINE INFORMATION (include gently):
- {helpline['name']}: {helpline['number']} ({helpline['hours']})
- International resources: findahelpline.com

INSTRUCTIONS:
1. Generate response in Anne's warm, nurturing, attuned voice
2. Validate their exhaustion and pain with deep empathy
3. Gently encourage professional support without alarming
4. Mention the helpline as a resource they can access
5. Allow the conversation to continue
6. Keep it under 150 words

Generate Anne's supportive response now:
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": warning_prompt}],
                temperature=0.8,
                max_tokens=250
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"""I can hear how empty and exhausted this feels for you right now. It sounds like you've been carrying a lot on your own, and that can be so isolating.

Even though it may not feel urgent, this is still something that deserves gentle care. Sometimes talking with a therapist or counselor can help you find new lightness—you don't have to do it alone.

If you'd like to talk to someone, you can reach out to {helpline['name']} at {helpline['number']} ({helpline['hours']}), or visit findahelpline.com for other options.

Let's take this as a reminder that your feelings matter and that help is available."""
    
    def reset_session(self):
        """Reset conversation for a new session"""
        self.conversation_history = []
        self.is_new_session = True
        self._cached_welcome = None
        self.session_blocked = False
    
    def get_conversation_history(self):
        """Return full conversation history"""
        return self.conversation_history


# Helper function for easy import
def create_anne_coach(user_country_code="US"):
    """
    Factory function to create a new Anne coach instance
    Args:
        user_country_code: ISO country code for helpline localization
    """
    return AnneRosentalCoach(user_country_code)