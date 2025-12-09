# Sports Abhyas 🏋️

Your AI-powered fitness companion that generates personalized workout and diet plans tailored to your goals.

## Features

- **Personalized Assessment** – AI analyzes your physique and health profile
- **Custom Diet Plans** – Indian vegetarian/non-vegetarian meal plans
- **Tailored Workouts** – Gym or calisthenics routines based on experience level
- **PDF Export** – Download your complete fitness plan
- **Smart AI** – Powered by Groq API with advanced language models

## Project Structure

```
sports_ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # Documentation
```

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd sports_ai

# Install dependencies
pip install -r requirements.txt
```

## Setup

Create a `.streamlit/secrets.toml` file in your project directory:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

Get your API key from [Groq Cloud](https://console.groq.com/).

## Usage

```bash
streamlit run app.py
```

1. Enter your physical details (height, weight, age)
2. Select your fitness goal and preferences
3. Choose diet type (vegetarian/non-vegetarian)
4. Pick workout style (gym/calisthenics)
5. Click **Generate Plan** and get your personalized fitness blueprint
6. Download as PDF for easy reference

## Input Options

- **Goals:** Build Muscle, Lose Fat, Get Toned, Maintain
- **Diet:** Vegetarian or Non-Vegetarian (Indian meals)
- **Workout:** Gym-based or Calisthenics
- **Levels:** Beginner, Intermediate, Advanced

## Output Structure

Your plan includes three sections:
- **Assessment** – Health and physique analysis
- **Diet Plan** – Full-day Indian meal breakdown
- **Workout Plan** – Weekly exercise routine

## Requirements

- Python 3.8+
- Streamlit
- Groq API key (free tier available)
- Internet connection for API calls

## Notes

- Plans are generated using AI and should complement professional medical advice
- PDF uses Latin-1 encoding for broad compatibility
- All data is processed securely through Groq's API

---

*Transform your physique today | Made by Shivank*
