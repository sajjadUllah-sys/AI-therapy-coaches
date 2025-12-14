# 🧠 AI Coaching Platform

A sophisticated multi-coach AI platform offering personalized coaching experiences through two distinct coaching personalities: **Dr. Anne Rosental** (emotionally attuned, nurturing) and **Hiro Lin** (action-oriented, pragmatic). Built with OpenAI GPT-4 and Streamlit.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-FF4B4B.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features

### Two Distinct Coaching Personalities

#### 👵 Dr. Anne Rosental
- **Background**: 65-year-old senior psychologist with 35+ years experience
- **Approach**: Humanistic Psychology, Gestalt Therapy, Emotion-Focused Therapy
- **Style**: Warm, nurturing, emotionally attuned
- **Best for**: Emotional exploration, self-compassion, inner child work, processing feelings
- **Communication**: Short, gentle responses with imagery and soft invitations

#### 🎯 Hiro Lin
- **Background**: 45-year-old executive coach with 20 years experience
- **Approach**: Cognitive Behavioral Therapy (CBT), Solution-Focused Coaching
- **Style**: Direct, focused, action-oriented
- **Best for**: Breaking through procrastination, decision-making, goal achievement, habit formation
- **Communication**: Concise, logical responses with clear next steps

### 🛡️ Comprehensive Safety System

The platform includes a robust **two-tier safety protocol**:

- **🚨 RED ZONE (Crisis Detection)**:
  - Suicidal thoughts, self-harm, violence
  - Immediately blocks session
  - Provides country-specific crisis helplines
  - Compassionate but firm intervention

- **⚠️ AMBER ZONE (Early Warning)**:
  - Depression signs, severe exhaustion, emotional numbness
  - Gentle professional help recommendations
  - Allows conversation to continue
  - Preventive care approach

- **🌍 Localized Support**:
  - Country-specific helplines (US, UK, Germany, Bangladesh)
  - International fallback resources
  - Dynamic helpline integration

### 📋 20 Coaching Scenarios

Each coach handles 20 distinct psychological scenarios:

1. Emotional Overwhelm
2. Self-Doubt and Inner Criticism
3. Loss of Motivation
4. Decision Anxiety
5. Sleep Issues and Racing Thoughts
6. Relationship Conflict
7. Procrastination and Avoidance
8. Boundary Struggles
9. Career or Purpose Doubt
10. Setback, Loss, or Failure
11. Feeling Stuck or Stagnant
12. Externalizing Responsibility
13. Overthinking and Analysis Paralysis
14. Breakthrough Moments
15. Relapse or Pattern Return
16. Anxiety and Worry
17. Loneliness and Isolation
18. Grief and Loss
19. Anger and Resentment
20. Identity Crisis or Transition

### 🏗️ Modular Architecture

- **Easy to extend**: Add new coaches by creating prompt and coach files
- **Shared safety protocol**: Consistent safety measures across all coaches
- **Clean separation**: Scenario definitions, coaching logic, and UI are separate
- **Factory pattern**: Simple coach instantiation

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-coaching-platform.git
   cd ai-coaching-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.template .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-openai-api-key-here
   ```

4. **Run the application**
   ```bash
   streamlit run coaching_app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

---

## 📖 Usage

### Getting Started

1. **Select Your Location**: Choose your country from the sidebar (for appropriate crisis helplines)
2. **Choose a Coach**: 
   - Select **Dr. Anne Rosental** for emotional exploration and gentle guidance
   - Select **Hiro Lin** for action-oriented coaching and clear strategies
3. **Start Coaching**: Begin sharing what's on your mind
4. **Switch Anytime**: Change coaches or start a new session whenever needed

### Example Conversations

#### With Dr. Anne Rosental:
```
You: I feel completely overwhelmed with everything going on.

Anne: That sounds like a lot of weight to carry, and I can imagine how 
exhausting that must feel. Perhaps we could slow down for a moment and 
just notice what feels most present right now—what's pulling at you the 
hardest?
```

#### With Hiro Lin:
```
You: I feel completely overwhelmed with everything going on.

Hiro: Alright, let's bring structure into this. What's one concrete thing 
that feels most urgent—or easiest to start with? Name it and we'll break 
it down.
```

---

## 🏗️ Project Structure

```
ai-coaching-platform/
│
├── coaching_app.py                 # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.template                   # Environment variables template
│
├── anne_rosental_prompt.py         # Anne's scenarios & system prompt
├── anne_rosental_coach.py          # Anne's coaching logic
│
├── hiro_lin_prompt.py              # Hiro's scenarios & system prompt
├── hiro_lin_coach.py               # Hiro's coaching logic
│
└── README.md                       # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `coaching_app.py` | Streamlit UI with coach selection and chat interface |
| `anne_rosental_prompt.py` | Anne's coaching scenarios, safety protocols, system prompt |
| `anne_rosental_coach.py` | Anne's conversation logic, API integration, safety handling |
| `hiro_lin_prompt.py` | Hiro's coaching scenarios and system prompt |
| `hiro_lin_coach.py` | Hiro's conversation logic, API integration, safety handling |
| `requirements.txt` | Python package dependencies |
| `.env.template` | Template for environment variables |

---

## 🔧 Adding a New Coach

The platform is designed for easy expansion. To add a new coach:

1. **Create prompt file** (`new_coach_prompt.py`):
   ```python
   class NewCoachScenarios:
       # Define 20 coaching scenarios
       scenario1 = {...}
   
   class NewCoachSystemPrompt:
       base_prompt = """Your coach's personality and approach..."""
   ```

2. **Create coach file** (`new_coach_coach.py`):
   ```python
   from new_coach_prompt import NewCoachScenarios, NewCoachSystemPrompt
   from anne_rosental_prompt import SafetyProtocol  # Shared safety
   
   class NewCoach:
       # Implement coaching logic
       pass
   
   def create_new_coach(user_country_code="US"):
       return NewCoach(user_country_code)
   ```

3. **Update `coaching_app.py`**:
   - Import the new coach
   - Add coach card to sidebar
   - Add coach to selection logic

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Supported Countries

| Code | Country | Helpline |
|------|---------|----------|
| `US` | United States | 988 Suicide & Crisis Lifeline |
| `GB` | United Kingdom | Samaritans (116 123) |
| `DE` | Germany | TelefonSeelsorge (0800 111 0 111) |
| `BD` | Bangladesh | Kaan Pete Roi (09612-784784) |
| Default | International | findahelpline.com |

---

## 🛡️ Safety & Ethics

### Important Disclaimers

⚠️ **This platform is NOT a substitute for:**
- Professional mental health care
- Medical advice or treatment
- Emergency services
- Crisis intervention

### When to Seek Professional Help

**Seek immediate help if you experience:**
- Thoughts of self-harm or suicide
- Plans to hurt yourself or others
- Severe depression or inability to function
- Psychotic experiences or hallucinations
- Severe trauma symptoms
- Substance abuse or addiction
- Domestic violence or abuse

### Crisis Resources

**United States**: 988 (Suicide & Crisis Lifeline)  
**United Kingdom**: 116 123 (Samaritans)  
**Germany**: 0800 111 0 111 (TelefonSeelsorge)  
**Bangladesh**: 09612-784784 (Kaan Pete Roi)  
**International**: [findahelpline.com](https://findahelpline.com)

---

## 🔒 Privacy & Data

- **No data storage**: Conversations are not saved to disk
- **Session-based**: All data is cleared when you close the app
- **OpenAI API**: Messages are sent to OpenAI for processing (see [OpenAI Privacy Policy](https://openai.com/policies/privacy-policy))
- **No tracking**: No analytics or user tracking

---

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- **Add new coaches**: Create additional coaching personalities
- **Expand scenarios**: Add more coaching situations
- **Improve safety**: Enhance crisis detection and responses
- **Add languages**: Internationalize the platform
- **Fix bugs**: Report and fix issues
- **Improve UI**: Enhance the user experience

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API Error"**
- Check that your API key is correct in `.env`
- Verify you have sufficient API credits
- Ensure you have internet connectivity

**"Module not found"**
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

**"Streamlit not found"**
- Install Streamlit: `pip install streamlit`
- Try running: `python -m streamlit run coaching_app.py`

**Chat not responding**
- Check your OpenAI API quota
- Verify `.env` file is in the project root
- Check terminal for error messages

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **Streamlit** for the amazing web framework
- **Anthropic** for Claude's assistance in development
- Inspired by therapeutic approaches from Carl Rogers, Fritz Perls, and modern CBT practitioners

---

## 📧 Contact

For questions, feedback, or support:

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-coaching-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-coaching-platform/discussions)
- **Email**: your.email@example.com

---

## ⭐ Support

If you find this project helpful, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with others who might benefit
- Contributing improvements or new features
- Reporting bugs or suggesting enhancements

---

**Remember**: This is a coaching tool for personal development, not a replacement for professional mental health care. If you're in crisis, please reach out to emergency services or a crisis helpline immediately.

---

<div align="center">
Made with ❤️ for personal growth and emotional wellbeing
</div>
