import streamlit as st
import requests
from fpdf import FPDF

# Load API Key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Function to request Groq API (Chat Completion)
def generate_plan(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "moonshotai/kimi-k2-instruct-0905",  # Your selected model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API Error {response.status_code}: {response.text}")

# PDF Generator
def create_pdf(plan_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_margins(20, 20, 20)

    cleaned_text = plan_text.replace('“', '"').replace('”', '"').replace("’", "'")
    cleaned_text = cleaned_text.replace('–', '-').replace('—', '-').replace('•', '*')

    for line in cleaned_text.split('\n'):
        try:
            safe_line = line.encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 8, safe_line)
        except:
            pdf.multi_cell(0, 8, "")

    return pdf.output(dest='S').encode('latin-1')

# Page configuration
st.set_page_config(page_title="Sports Abhyas", page_icon="🏋️", layout="wide", initial_sidebar_state="collapsed")

# Header
st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <h1>🏋️ Sports Abhyas</h1>
        <p style='color: #6c757d; font-size: 18px;'>Your AI-Powered Fitness Companion</p>
    </div>
""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("### Enter Your Details")

        goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Fat", "Get Toned", "Maintain"])
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        age = st.number_input("Age", min_value=16, max_value=100, value=25)

        diet_type = st.radio("Preferred Diet Type", ["Vegetarian", "Non-Vegetarian"], horizontal=True)
        workout_type = st.radio("Workout Type", ["Gym", "Calisthenics"], horizontal=True)
        level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])

        generate_button = st.button("Generate Plan", type="primary")

    with col2:
        if generate_button:
            with st.spinner("Crafting your personalized plan..."):
                prompt = f"""
                Analyze the user's details and craft a fitness plan.

                Goal: {goal}
                Height: {height} cm
                Weight: {weight} kg
                Age: {age}
                Diet Type: {diet_type}
                Workout Type: {workout_type}
                Experience Level: {level}

                Return result in this exact structured Markdown format:

                ### Assessment
                (Short physique & health analysis)

                ### Diet Plan
                (Full-day simple Indian {diet_type.lower()} meal plan)

                ### Workout Plan
                ({workout_type.lower()} based weekly plan for {level.lower()} level)
                analyze all data deeply and act like a personal fitness trainer and then give the result
                """

                try:
                    st.session_state['plan'] = generate_plan(prompt)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state['plan'] = None

        if 'plan' in st.session_state and st.session_state['plan']:
            plan = st.session_state['plan']

            tab1, tab2, tab3 = st.tabs(["Assessment", "Diet", "Workout"])

            with tab1:
                st.markdown(plan.split("### Diet Plan")[0])

            with tab2:
                st.markdown("### Diet Plan" + plan.split("### Diet Plan")[1].split("### Workout Plan")[0])

            with tab3:
                st.markdown("### Workout Plan" + plan.split("### Workout Plan")[1])

            pdf_bytes = create_pdf(plan)
            st.download_button(
                label="📥 Download Plan as PDF",
                data=pdf_bytes,
                file_name="Sports_Abhyas_Plan.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.info("👈 Fill details and click Generate Plan!")

st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 30px 0; font-size: 14px;'>
        Made by Shivank | Transform Your Physique Today
    </div>
""", unsafe_allow_html=True)
