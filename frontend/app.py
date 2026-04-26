import streamlit as st
import requests
import json

if "scores" not in st.session_state:
    st.session_state["scores"] = {}

API_URL = "https://skillgap-ai-pozg.onrender.com"

st.title("SkillGap AI")

# INPUT
jd = st.text_area("Paste Job Description")
# ADD THIS BLOCK HERE (UPLOAD FEATURE)
st.subheader("Upload Resume")

uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

# Initialize state
if "last_uploaded_file" not in st.session_state:
    st.session_state["last_uploaded_file"] = None

# Only process if NEW file uploaded
if uploaded_file is not None:

    if uploaded_file.name != st.session_state["last_uploaded_file"]:

        with st.spinner("Processing resume..."):

            res = requests.post(
                f"{API_URL}/upload-resume",
                files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                timeout=30
            ).json()

        if "resume_text" in res:
            st.session_state["resume_text"] = res["resume_text"]
            st.session_state["last_uploaded_file"] = uploaded_file.name

            st.success("Resume processed successfully!")


if "resume_skills" in st.session_state:
    st.markdown("### Extracted Skills")
    st.write(st.session_state["resume_skills"])

resume_input = st.text_area("Or paste resume text (optional)")

if st.button("Analyze"):
    resume_data = resume_input

    if "resume_text" in st.session_state:
        resume_data = " ".join(st.session_state["resume_text"])
    res = requests.post(f"{API_URL}/analyze", json={
        "jd": jd,
        "resume": resume_data
    }).json()

    st.session_state["jd_skills"] = res["jd_skills"]

    st.success("Skills Extracted")

    st.markdown("### JD Skills")
    st.write(res["jd_skills"])

    st.markdown("### Resume Skills")
    st.write(res["resume_skills"])

# ASSESSMENT
scores = st.session_state["scores"]

if "jd_skills" in st.session_state:
    skills = st.session_state["jd_skills"]

    for skill in skills:
        st.subheader(f"Skill: {skill}")

        # Store questions
        if f"questions_{skill}" not in st.session_state:
            q = requests.post(
                f"{API_URL}/questions",
                params={"skill": skill}
            ).json()

            st.session_state[f"questions_{skill}"] = q["questions"]
        
       
            

        # Show questions
        questions = st.session_state[f"questions_{skill}"]

       
        parsed = None

        try:
            if isinstance(questions, str):
                parsed = json.loads(questions)
            else:
                parsed = questions
        except:
            parsed = None

        # Clean UI display
        if parsed:
            st.markdown("### Basic")
            st.markdown(f"- {parsed.get('basic', 'Not available')}")

            st.markdown("### Intermediate")
            st.markdown(f"- {parsed.get('intermediate', 'Not available')}")

            st.markdown("### Advanced")
            st.markdown(f"- {parsed.get('advanced', 'Not available')}")

        else:
            st.warning("Could not format questions properly")
            st.write(questions)

        print(questions)

    
        if st.button(f"Generate More Questions ({skill})", key=f"regen_{skill}"):

            with st.spinner("Generating new questions..."):
                q = requests.post(
                    f"{API_URL}/questions",
                    params={"skill": skill}
                ).json()

            st.session_state[f"questions_{skill}"] = q["questions"]

            st.success("New questions generated!")

        answer = st.text_area(f"Answer for {skill}", key=f"ans_{skill}")

        if st.button(f"Evaluate {skill}", key=f"btn_{skill}"):
            res = requests.post(
                f"{API_URL}/evaluate",
                params={"skill": skill, "answer": answer}
            ).json()

            

            try:
                parsed = json.loads(res["result"])

                score = parsed.get("score", 0)
                feedback = parsed.get("feedback", "")

                st.markdown(f"### Score: {score} / 10")

                st.markdown("### Feedback")

                # Split feedback into points (optional enhancement)
                points = feedback.split(". ")

                for point in points:
                    if point.strip():
                        st.markdown(f"- {point.strip()}")

                # Save score
                st.session_state["scores"][skill] = score

            except:
                st.error("Could not parse evaluation result")
                st.write(res["result"])

    if st.button("Generate Final Report"):
        final = requests.post(
    f"{API_URL}/final-report",
    json=st.session_state["scores"]
).json()

        st.success("Final Report")
        st.markdown("## Final Report")

        st.markdown(f"### Final Score: {final['final_score']}")
        st.markdown(f"### Skill Gaps: {', '.join(final['gaps']) if final['gaps'] else 'None'}")

        st.markdown("### Learning Plan")
        st.markdown(final["learning_plan"])