import streamlit as st
from groq import Groq
from fpdf import FPDF

# Set your Groq API Key here
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

# Page configuration
st.set_page_config(page_title="Sports Abhyas", page_icon="🏋️", layout="wide", initial_sidebar_state="collapsed")

# Header
st.markdown("""
    <div style='text-align: center; padding: 30px 0;'>
        <h1>🏋️ Sports Abhyas</h1>
        <p style='color: #6c757d; font-size: 18px;'>Your AI-Powered Fitness Companion</p>
    </div>
""", unsafe_allow_html=True)

# PDF Generator
def create_pdf(plan_text):
    pdf = FPDF()
    pdf.add_page()
    
    # Use DejaVu font which supports Unicode characters
    # For Streamlit, we'll handle special characters better
    pdf.set_font("Arial", size=12)
    pdf.set_margins(20, 20, 20)
    
    # Clean the text to remove problematic characters
    # Replace smart quotes and other special characters
    cleaned_text = plan_text.replace('"', '"').replace('"', '"')
    cleaned_text = cleaned_text.replace(''', "'").replace(''', "'")
    cleaned_text = cleaned_text.replace('–', '-').replace('—', '-')
    cleaned_text = cleaned_text.replace('•', '*')
    cleaned_text = cleaned_text.replace('…', '...')
    
    # Split into lines and add each line
    for line in cleaned_text.split('\n'):
        try:
            # Try to encode as latin-1, replace characters that can't be encoded
            safe_line = line.encode('latin-1', 'ignore').decode('latin-1')
            pdf.multi_cell(0, 8, safe_line)
        except:
            # If there's still an error, skip the line
            pdf.multi_cell(0, 8, "")
    
    return pdf.output(dest='S').encode('latin-1')

# Main UI
with st.container():
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("### Enter Your Details")

        goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Fat", "Get Toned", "Maintain"])
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        age = st.number_input("Age", min_value=16, max_value=100, value=25)

        # New options
        diet_type = st.radio("Preferred Diet Type", ["Vegetarian", "Non-Vegetarian"], horizontal=True)
        workout_type = st.radio("Workout Type", ["Gym", "Calisthenics"], horizontal=True)
        level = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])

        generate_button = st.button("Generate Plan", type="primary")

    with col2:
        # Generate plan when button is clicked
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
                (Short physique & health analysis based on age, weight, height, and goal)

                ### Diet Plan
                (Provide a full-day simple Indian {diet_type.lower()} meal plan suitable for the goal)

                ### Workout Plan
                (Design a {workout_type.lower()}-based weekly schedule tailored for a {level.lower()} individual)
                deeply analyze all things and dont give same plan for all types be some unique 
                """

                try:
                    response = client.chat.completions.create(
                        model="moonshotai/kimi-k2-instruct-0905",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response.choices[0].message.content
                    st.session_state['plan'] = result

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.session_state['plan'] = None

        # Display tabs (this will show updated content after generation)
        if 'plan' in st.session_state and st.session_state['plan']:
            plan = st.session_state['plan']
            
            tab1, tab2, tab3 = st.tabs(["Assessment", "Diet", "Workout"])

            with tab1:
                if "### Diet Plan" in plan:
                    assessment_section = plan.split("### Diet Plan")[0]
                    st.markdown(assessment_section)
                else:
                    st.markdown(plan)

            with tab2:
                if "### Diet Plan" in plan and "### Workout Plan" in plan:
                    diet_section = plan.split("### Diet Plan")[1].split("### Workout Plan")[0]
                    st.markdown("### Diet Plan" + diet_section)
                else:
                    st.info("Diet plan section not found")

            with tab3:
                if "### Workout Plan" in plan:
                    workout_section = plan.split("### Workout Plan")[1]
                    st.markdown("### Workout Plan" + workout_section)
                else:
                    st.info("Workout plan section not found")

            # PDF Download Button
            pdf_bytes = create_pdf(plan)
            st.download_button(
                label="📥 Download Plan as PDF",
                data=pdf_bytes,
                file_name="Sports_Abhyas_Plan.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.info("👈 Fill in your details and click 'Generate Plan' to get started!")

# Footer
st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 30px 0; font-size: 14px;'>
        Made by Shivank | Transform Your Physique Today
    </div>
""", unsafe_allow_html=True)
