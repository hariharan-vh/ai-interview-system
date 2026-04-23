import streamlit as st
import sqlite3
import time
import speech_recognition as sr
from gtts import gTTS
from PyPDF2 import PdfReader
from PIL import Image
import pandas as pd
import random
import smtplib
from email.mime.text import MIMEText

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Interview", layout="wide")

# ---------------- DB ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
c.execute("""CREATE TABLE IF NOT EXISTS candidates(
    firstname TEXT, lastname TEXT, phone TEXT, email TEXT, whatsapp TEXT
)""")
conn.commit()

# ---------------- EMAIL FUNCTION ----------------
def send_email(to_email, message):
    EMAIL = "vhariharan1415@gmail.com"        # 🔴 replace
    PASSWORD = "gigp fqxw grbi fnst"        # 🔴 replace

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)

        msg = MIMEText(message)
        msg["Subject"] = "Interview Result"
        msg["From"] = EMAIL
        msg["To"] = to_email

        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# ---------------- THEME ----------------
theme = st.sidebar.toggle("🌗 Dark Mode")
if theme:
    st.markdown("<style>.stApp {background:#0e1117;color:white;}</style>", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
with col2:
    st.markdown("<h1>MIDDLE CLASS.pvt.ltd.</h1>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
defaults = {
    "login": False,
    "user": "",
    "skills": [],
    "q_index": 0,
    "started": False,
    "history": [],
    "answers": [],
    "feedbacks": [],
    "questions": [],
    "resume_type": "Fresher",
    "resume_score": 0,
    "form_submitted": False
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

# ---------------- DASHBOARD ----------------
def dashboard():
    st.subheader("🏢 Company Dashboard")

    names = ["Rahul","Priya","Arjun","Sneha","Karthik"]

    st.markdown("### 🏆 Top Performers")
    for n in names:
        st.success(f"{n} - {random.randint(80,100)} Score")

    st.markdown("### 🎖 Best Performer")
    st.info(random.choice(names))

    st.markdown("### 💼 Roles")
    st.write("Python Developer, AI Engineer, Data Analyst")

    st.markdown("### 💰 Salary")
    st.write("3 LPA - 12 LPA")

# ---------------- FACE CAPTURE ----------------
def face_capture():
    st.subheader("📸 Face Capture")
    img = st.camera_input("Capture your face")

    if img:
        image = Image.open(img)
        image.save(f"{st.session_state.user}_face.jpg")
        st.success("Face captured successfully")

# ---------------- RESUME ----------------
def extract_skills(text):
    db = ["python","java","ai","ml","data","sql"]
    return list(set([s for s in db if s in text.lower()]))

def resume():
    st.subheader("📄 Resume Analysis")

    st.session_state.resume_type = st.selectbox("Resume Type",["Fresher","Experienced"])

    file = st.file_uploader("Upload Resume", type=["pdf"])

    if file:
        reader = PdfReader(file)
        text = "".join([p.extract_text() for p in reader.pages])

        skills = extract_skills(text)
        st.session_state.skills = skills

        score = len(skills)*10
        if st.session_state.resume_type == "Experienced":
            score += 10

        st.session_state.resume_score = min(score,100)

        st.success("Resume Processed")
        st.write("Skills:", skills)
        st.progress(st.session_state.resume_score/100)

# ---------------- VOICE ----------------
def speak(text):
    gTTS(text=text, lang="en").save("voice.mp3")
    st.audio("voice.mp3", autoplay=True)

# ---------------- LISTEN ----------------
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as src:
            audio = r.listen(src, timeout=10, phrase_time_limit=30)
            return r.recognize_google(audio)
    except:
        return st.text_input("🎤 Type your answer:")

# ---------------- QUESTIONS ----------------
def generate_questions():
    base = ["Tell me about yourself","What are your strengths?","Why should we hire you?"]
    skill_q = [f"Explain {s}" for s in st.session_state.skills]
    return random.sample(skill_q + base, min(len(skill_q + base), 5))

# ---------------- FEEDBACK ----------------
def answer_feedback(ans):
    if len(ans.split()) > 15:
        return "🌟 Excellent answer"
    elif len(ans.split()) > 7:
        return "👍 Good answer"
    else:
        return "⚠️ Improve your answer"

# ---------------- INTERVIEW ----------------
def interview():
    st.subheader("🎭 AI Interview")

    if not st.session_state.started:
        if st.button("Start Interview"):
            st.session_state.started = True
            st.session_state.questions = generate_questions()

    if st.session_state.started:

        if st.session_state.q_index < len(st.session_state.questions):

            q = st.session_state.questions[st.session_state.q_index]

            st.markdown(f"🤖 {q}")
            speak(q)

            timer = st.empty()
            for i in range(10,0,-1):
                if i <= 5:
                    timer.warning(f"⚠️ Thinking Time: {i}s")
                else:
                    timer.info(f"Thinking Time: {i}s")
                time.sleep(1)

            timer.warning("🎤 Speak Now (30s)")

            ans = listen()

            if ans:
                st.write("🧑 You:", ans)

                st.session_state.answers.append(ans)

                sc = 10 if len(ans.split()) > 5 else 0
                st.session_state.history.append(sc)

                fb = answer_feedback(ans)
                st.session_state.feedbacks.append(fb)

                st.success(fb)

                time.sleep(2)
                st.session_state.q_index += 1
                st.rerun()

        else:
            st.success("🎉 Interview Completed")

            final_score = sum(st.session_state.history)*10
            st.write(f"Final Score: {final_score}")

 # ✅ NEW FEATURE: USER DETAILS FORM
            if not st.session_state.form_submitted:
                st.subheader("📝 Enter Your Details")

                fname = st.text_input("First Name", key="fname") 
                lname = st.text_input("Last Name", key="lname")
                phone = st.text_input("Phone Number", key="phone")
                email_input = st.text_input("Email ID", key="email1")
                whatsapp = st.text_input("WhatsApp Number", key="whatsapp")

                if st.button("Submit Details"):
                    if fname and lname and phone and email_input:
                        c.execute("INSERT INTO candidates VALUES (?,?,?,?,?)",
                                  (fname, lname, phone, email_input, whatsapp))
                        conn.commit()

                        st.success("✅ Details Saved Successfully")
                        st.session_state.form_submitted = True
                    else:
                        st.error("⚠️ Please fill all required fields")

 # ✅ SELECTION LOGIC
            if final_score >= 60:
                st.success("✅ SELECTED")

                st.subheader("📝 Enter Email to Receive Offer")

                email = st.text_input("Enter Email Again", key="email2")

                if st.button("Send Offer Letter"):
                    msg = f"""
Hii, Thank you taking an interest in new job opportunities at MIDDLE CLASS.pvt.ltd.The following roles have been added: Jobs
Audit Manager - Techonology & Operations
App Development
Web Development
Game Development
AI Product Owner
Analyst,Product Control(MBA Fresher)
   
   You are receiving these emails because you finished Online-AI-Interview in 2026 job roles.
You can Manage your Job alert here. Places are Alocated in Bangalore,Chennai,Hydrabad IND.

Congratulations!

You are selected in MIDDLE CLASS.pvt.ltd.
Package: 6 LPA

HR will contact you soon.

Regards : V.Hariharan
contact : +917010864457

Please do not reply to this email as it is system generated.
Stay in touch with MIDDLE CLASS.pvt.ltd.
"""

                    if send_email(email, msg):
                        st.success("📧 Offer Letter Sent Successfully")
                    else:
                        st.error("Email sending failed")

            else:
                st.error("❌ NOT SELECTED")
                st.warning("Interview Closed")

# ---------------- FLOW ----------------
if not st.session_state.login:
    login()
else:
    menu = st.sidebar.radio("Menu",["Dashboard","Face Capture","Resume","Interview"])

    if menu=="Dashboard":
        dashboard()
    elif menu=="Face Capture":
        face_capture()
    elif menu=="Resume":
        resume()
    elif menu=="Interview":
        interview()
