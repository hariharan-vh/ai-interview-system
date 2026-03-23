import streamlit as st
import sqlite3
import time
import random
import speech_recognition as sr
from gtts import gTTS
from PyPDF2 import PdfReader
from PIL import Image
import os
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Interview", layout="wide")

# ---------------- DB ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS scores(username TEXT, score INTEGER)")
conn.commit()

# ---------------- THEME ----------------
theme = st.sidebar.toggle("🌗 Dark Mode")

if theme:
    st.markdown("""
    <style>
    .stApp {background:#0e1117;color:white;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {background:white;color:black;}
    </style>
    """, unsafe_allow_html=True)

# ---------------- ANIMATION + LOGO ----------------
st.markdown("""
<style>
.fade-in {
    animation: fadeIn 1.5s ease-in;
}
@keyframes fadeIn {
    from {opacity:0;}
    to {opacity:1;}
}
.card {
    padding:20px;
    border-radius:15px;
    box-shadow:0 4px 10px rgba(0,0,0,0.2);
    margin:10px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
with col2:
    st.markdown("<h1 class='fade-in'>MIDDLE CLASS.pvt.ltd.</h1>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
defaults = {
    "login": False,
    "user": "",
    "face": False,
    "skills": [],
    "score": 0,
    "q_index": 0,
    "started": False
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- LOGIN ----------------
def login():
    st.subheader("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        res = c.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p)).fetchone()
        if res:
            st.session_state.login = True
            st.session_state.user = u
        else:
            c.execute("INSERT INTO users VALUES (?,?)",(u,p))
            conn.commit()
            st.success("User Registered")

# ---------------- FACE ----------------
def face_capture():
    st.subheader("📸 Face Setup")
    img = st.camera_input("Capture Face")
    if img:
        Image.open(img).save(f"{st.session_state.user}.jpg")
        st.success("Face Stored")
        st.session_state.face = True

def face_verify():
    st.subheader("🔍 Face Verify")
    img = st.camera_input("Verify Face")
    if img and os.path.exists(f"{st.session_state.user}.jpg"):
        st.success("Face Verified ✅")
        st.session_state.face = True

# ---------------- RESUME ----------------
def extract_skills(text):
    db = ["python","java","ai","ml","data","sql","web","cloud"]
    return [s for s in db if s in text.lower()]

def resume():
    st.subheader("📄 Resume Upload")
    file = st.file_uploader("Upload PDF", type=["pdf"])
    st.selectbox("Resume Type",["Fresher","Experienced"])

    if file:
        reader = PdfReader(file)
        text = "".join([p.extract_text() for p in reader.pages])
        st.session_state.skills = extract_skills(text)
        st.success("Resume Processed")
        st.write("Skills:", st.session_state.skills)

# ---------------- VOICE ----------------
def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("voice.mp3")
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)
    st.audio("voice.mp3")

# ---------------- STT ----------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as src:
        audio = r.listen(src, timeout=5)
        try:
            return r.recognize_google(audio)
        except:
            return ""

# ---------------- QUESTIONS ----------------
def get_questions():
    base = [
        "What is AI?",
        "Explain Python",
        "What is database?"
    ]
    if st.session_state.skills:
        return [f"Explain {s}" for s in st.session_state.skills[:3]]
    return base

# ---------------- EVALUATION ----------------
def evaluate(ans):
    return (10,"Good 👍") if len(ans.split()) > 5 else (0,"Wrong ❌")

# ---------------- JOB ----------------
def jobs():
    st.subheader("💼 Job Offers")
    job_db = {
        "python":"Python Dev (4-8 LPA)",
        "ai":"AI Engineer (6-12 LPA)",
        "ml":"ML Engineer (5-10 LPA)"
    }
    for s in st.session_state.skills:
        if s in job_db:
            st.success(job_db[s])

# ---------------- INTERVIEW ----------------
def interview():
    st.subheader("🎭 AI Interview")

    questions = get_questions()

    if not st.session_state.started:
        if st.button("Start Interview 🚀"):
            st.session_state.started = True

    if st.session_state.started and st.session_state.q_index < len(questions):

        q = questions[st.session_state.q_index]
        st.markdown(f"<div class='card fade-in'>🤖 {q}</div>", unsafe_allow_html=True)
        speak(q)

        timer = st.empty()
        for i in range(30,0,-1):
            if i <= 10:
                timer.error(f"⚠️ Hurry up! {i}s")
            else:
                timer.info(f"Thinking Time: {i}s")
            time.sleep(1)

        ans = listen()
        st.write("You:", ans)

        sc, fb = evaluate(ans)
        st.session_state.score += sc

        st.success(fb)
        st.write("Score:", st.session_state.score)

        st.session_state.q_index += 1
        time.sleep(2)
        st.rerun()

    elif st.session_state.q_index >= 3:
        st.success("🎉 Interview Completed")

        st.write("Final Score:", st.session_state.score)

        if st.session_state.score >= 20:
            st.success("🌟 Excellent Performance")
        elif st.session_state.score >= 10:
            st.info("👍 Good Performance")
        else:
            st.error("❌ Needs Improvement")

        st.subheader("📊 Score Visualization")

        df = pd.DataFrame({
            "Stage": ["Q1", "Q2", "Q3"],
            "Score": [st.session_state.score/3]*3
        })

        st.bar_chart(df.set_index("Stage"))

        c.execute("INSERT INTO scores VALUES (?,?)",(st.session_state.user,st.session_state.score))
        conn.commit()

# ---------------- FLOW ----------------
if not st.session_state.login:
    login()
else:
    menu = st.sidebar.radio("Menu",["Face Setup","Face Verify","Resume","Interview","Jobs"])

    if menu=="Face Setup":
        face_capture()
    elif menu=="Face Verify":
        face_verify()
    elif menu=="Resume":
        resume()
    elif menu=="Interview":
        interview()
    elif menu=="Jobs":
        jobs()