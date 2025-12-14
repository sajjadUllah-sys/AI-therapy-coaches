"""
Hiro Lin AI Coaching System
Main class that handles conversation logic and OpenAI integration
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from hiro_lin_prompt import HiroLinScenarios, HiroLinSystemPrompt
from anne_rosental_prompt import SafetyProtocol  # Shared safety protocol

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class HiroLinCoach:
    """
    Main coaching class for Hiro Lin
    Handles conversation flow, scenario detection, and safety protocols
    """
    
    def __init__(self, user_country_code="US"):
        self.conversation_history = []
        self.scenarios = HiroLinScenarios()
        self.safety = SafetyProtocol()
        self.system_prompt = HiroLinSystemPrompt.base_prompt
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
                     "greetings", "hallo", "hi hiro", "hello hiro", "hey hiro"]
        user_message_lower = user_message.lower().strip()
        return any(greeting in user_message_lower for greeting in greetings)
    
    def get_welcome_message(self):
        """Get welcome message - generates once and caches"""
        if self._cached_welcome is None:
            self._cached_welcome = self._generate_welcome()
        return self._cached_welcome
    
    def _generate_welcome(self):
        """Generate personalized welcome message from Hiro using GPT-4"""
        welcome_prompt = f"""{self.system_prompt}

You are greeting a new client who just selected you as their coach for the first time.

Generate a brief, focused welcome message (1-2 sentences maximum) that:
- Introduces yourself as Hiro Lin naturally
- Sets an action-oriented but warm tone
- Is concise and professional
- Sounds like a real executive coach, not an AI

Keep it SHORT and punchy - just a clear hello and invitation.
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
            return "Hey, I'm Hiro Lin. Let's figure out what you need and get you moving forward."
    
    def generate_response(self, user_message):
        """
        Generate Hiro's response based on user message
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

SITUATION CONTEXT:
{matched_scenario['context']}

COACHING FOCUS AREAS:
"""
            for focus in matched_scenario['coaching_focus']:
                enhanced_prompt += f"- {focus}\n"
            
            enhanced_prompt += f"""
IMPORTANT: 
- This scenario description is for YOUR understanding only—do NOT reference it explicitly to the client
- Respond naturally as Hiro would, drawing on this coaching framework
- Stay focused on what the client is actually saying
- Follow your conversational rhythm: clarify + challenge/reframe + activate with next step
- Keep it SHORT and PUNCHY - 2-4 sentences maximum
- Be direct but respectful, action-oriented but caring

The client's exact words: "{user_message}"

What's the core issue here? What needs to shift? Respond as Hiro would naturally.
"""
        else:
            enhanced_prompt += f"""NO SPECIFIC SCENARIO DETECTED

The client shared: "{user_message}"

GUIDANCE:
- Get to the heart of what they're saying quickly
- What's the real obstacle or pattern here?
- Respond naturally as Hiro would, drawing on your coaching expertise
- Follow your conversational rhythm: clarify + challenge/reframe + activate
- Keep it SHORT and PUNCHY - 2-4 sentences maximum
- Be direct, pragmatic, and focused on forward movement

Remember: You're helping someone solve a real problem with real constraints. Get them moving.
"""
        
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": enhanced_prompt}] + self.conversation_history,
                temperature=0.7,  # Slightly lower for more focused responses
                max_tokens=250,  # Shorter for Hiro's concise style
                presence_penalty=0.2,
                frequency_penalty=0.2
            )
            
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
            
        except Exception as e:
            return f"Having trouble connecting right now. Try again in a moment. (Error: {str(e)})"
    
    def _generate_greeting(self):
        """Generate personalized greeting response from Hiro"""
        greeting_prompt = f"""{self.system_prompt}

A client just said hello/hi to you.

Generate a brief, focused greeting response (1-2 sentences) that:
- Returns their greeting naturally
- Sets an action-oriented tone
- Invites them to share what they need
- Sounds conversational and professional

Keep it SHORT and direct.
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
            return "Hey there. What brings you here today?"
    
    def _generate_crisis_response(self, user_message):
        """Generate dynamic crisis response with appropriate helpline"""
        helpline = self.safety.get_helpline_for_country(self.user_country_code)
        
        crisis_prompt = f"""{self.system_prompt}

=== CRITICAL SAFETY SITUATION ===

The client just shared: "{user_message}"

SITUATION: Client has expressed thoughts of self-harm, suicide, violence, or immediate danger.

RESPONSE REQUIREMENTS:
- Respond with calm authority and protective care
- Acknowledge the severity clearly and directly
- State firmly that this requires professional help immediately
- Provide specific helpline numbers
- End the conversation to prioritize their safety
- Use Hiro's clear, calm, protective voice

HELPLINE INFORMATION (MUST include this exactly):
- Helpline Name: {helpline['name']}
- Number: {helpline['number']}
- Hours: {helpline['hours']}
- International resources: findahelpline.com

CRITICAL INSTRUCTIONS:
1. Generate a response in Hiro's calm, clear, authoritative voice
2. Be direct about the seriousness
3. Provide clear action steps
4. Include the helpline information above
5. End by firmly pausing the conversation
6. Keep it under 200 words but clear and caring

Generate Hiro's crisis response now:
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
            return f"""Hey, I can tell this situation feels really heavy—and I take that seriously.

From what you're describing, this goes beyond what I can safely support you with here. Right now, the most important step is to connect with professional help immediately.

If you're in danger or thinking about hurting yourself, please contact:
- {helpline['name']}: {helpline['number']} ({helpline['hours']})
- International helplines: findahelpline.com
- Emergency services: Call your local emergency number

You don't have to handle this on your own—professional help is available right now. Please reach out. That's the right move for your safety.

I'll pause here so you can focus on getting real support. You're not alone in this."""
    
    def _generate_warning_response(self, user_message):
        """Generate dynamic warning response for amber zone situations"""
        helpline = self.safety.get_helpline_for_country(self.user_country_code)
        
        warning_prompt = f"""{self.system_prompt}

=== EARLY WARNING SITUATION ===

The client shared: "{user_message}"

SITUATION: Client shows warning signs of depression or distress but not immediate crisis.

RESPONSE REQUIREMENTS:
- Validate their exhaustion pragmatically
- Normalize seeking professional support
- Encourage proactive help-seeking
- Mention helpline as resource
- Allow conversation to continue
- Use Hiro's calm, practical, preventive voice

HELPLINE INFORMATION (include gently):
- {helpline['name']}: {helpline['number']} ({helpline['hours']})
- International resources: findahelpline.com

INSTRUCTIONS:
1. Generate response in Hiro's clear, pragmatic, caring voice
2. Acknowledge they're running on empty
3. Frame professional help as smart, proactive move
4. Provide helpline info
5. Allow the conversation to continue
6. Keep it under 150 words

Generate Hiro's supportive response now:
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
            return f"""I can tell you're running on empty right now—that kind of exhaustion can sneak up on anyone. It's a sign that you've been pushing too hard for too long.

You don't have to wait until things get worse to ask for help. Talking with a professional can give you the tools and space to recharge before this turns into something heavier.

You can contact {helpline['name']} at {helpline['number']} ({helpline['hours']}), or check findahelpline.com for other options.

It's a smart move to get extra support early—that's what resilience really means."""
    
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
def create_hiro_coach(user_country_code="US"):
    """
    Factory function to create a new Hiro coach instance
    Args:
        user_country_code: ISO country code for helpline localization
    """
    return HiroLinCoach(user_country_code)