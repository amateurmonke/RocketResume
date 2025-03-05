import streamlit as st
import google.generativeai as genai
import os

api_key = os.getenv("GOOGLE_API_KEY")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash") 
except Exception as e:
    st.error(f"❌ Error initializing Gemini API: {str(e)}")
    st.stop()

def generate_resume(name, email, links, education, skills, projects, experience, awards):
    try:
        prompt = f"""
        Generate a professional resume for:
        - Name: {name}
        - Email: {email}
        - Github/Linkedin/Website: {links}
        - Education: {education}
        - Skills: {skills}
        - Projects: {projects}
        - Experience: {experience}
        - Awards & Honours: {awards}

        Format the resume in the above mentioned order, keeping it simple.
        Prioritize projects or experience based on what is more compelling. Elaborate on projects if the user has given adequate data.
        Separate multiple values with semicolons (;). Divide skills mentioned by the user into categories.
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"❌ Error generating resume: {str(e)}"

# Streamlit UI
st.title("🚀 RocketResume")

name = st.text_input("Full Name")
email = st.text_input("Email")
links = st.text_area("Links (Github/Linkedin/Website)")
st.markdown("> Separate values using semi-colons")  
education = st.text_area("Education")
skills = st.text_area("Skills")
projects = st.text_area("Projects")
experience = st.text_area("Work Experience")
awards = st.text_area("Awards & Honours")

if st.button("Generate Resume"):
    if name and education and skills:
        resume_text = generate_resume(name, email, links, education, skills, projects, experience, awards)
        st.markdown(f"### Generated Resume\n\n{resume_text}")
    else:
        st.error("Please fill in at least Name, Education, and Skills.")
