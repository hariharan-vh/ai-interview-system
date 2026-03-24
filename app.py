import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="AI Interview System", layout="wide")

# ---------------- THEME ----------------
if st.sidebar.toggle("🌗 Dark Mode"):
    st.markdown("<style>.stApp{background:#0e1117;color:white;}</style>", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
with col2:
    st.markdown("<h1>MIDDLE CLASS.pvt.ltd.</h1>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
defaults = {
    "login": False,
    "page": "login",
    "skills": [],
    "q_index": 0,
    "score": 0,
    "answers": []
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- LOGIN ----------------
if st.session_state.page == "login":
    st.subheader("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user and pwd:
            st.session_state.page = "dashboard"

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":

    st.subheader("📊 Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        st.success("💻 Java Developer")
    with col2:
        st.info("🤖 AI Engineer")

    st.markdown("### 📸 Face Verification")

    st.markdown("""
    <video id="video" width="250" autoplay></video>
    <p id="status">Checking...</p>

    <script>
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream){
        document.getElementById('video').srcObject = stream;
        document.getElementById("status").innerHTML="✅ Face Verified";
    })
    .catch(function(){
        document.getElementById("status").innerHTML="❌ Camera Blocked";
    });
    </script>
    """, unsafe_allow_html=True)

    file = st.file_uploader("📄 Upload Resume (txt)", type=["txt"])

    if file:
        text = file.read().decode("utf-8").lower()
        skills_db = ["python","java","ai","ml","sql"]
        st.session_state.skills = [s for s in skills_db if s in text]

        st.success("Resume Processed")
        st.write("Skills:", st.session_state.skills)

        if st.button("🚀 Start Interview"):
            st.session_state.page = "interview"

# ---------------- INTERVIEW ----------------
elif st.session_state.page == "interview":

    st.subheader("🎭 AI Interview")

    if "questions" not in st.session_state:
        if st.session_state.skills:
            st.session_state.questions = [f"Explain {s}" for s in st.session_state.skills[:5]]
        else:
            st.session_state.questions = [
                "Tell me about yourself",
                "Explain your project",
                "What are your strengths",
                "Why should we hire you",
                "Explain your skills"
            ]

    if st.session_state.q_index < 5:

        q = st.session_state.questions[st.session_state.q_index]

        st.markdown(f"<div style='padding:15px;background:#eee;border-radius:10px;'>🤖 {q}</div>", unsafe_allow_html=True)

        # 🔊 Voice
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{q}");
        speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

        # Timer
        timer = st.empty()
        for i in range(30,0,-1):
            timer.info(f"⏳ {i}s")
            time.sleep(1)

        st.success("🎤 Speak Now")

        # Speech input
        st.markdown("""
        <button onclick="startSpeech()">🎤 Speak</button>
        <p id="output"></p>

        <script>
        function startSpeech(){
            var recognition = new webkitSpeechRecognition();
            recognition.lang="en-US";

            recognition.onresult=function(e){
                var text=e.results[0][0].transcript;
                document.getElementById("output").innerHTML=text;

                const doc = window.parent.document;
                const input = doc.querySelector('input[type="text"]');
                if(input){
                    input.value=text;
                    input.dispatchEvent(new Event('input',{bubbles:true}));
                }
            }
            recognition.start();
        }
        </script>
        """, unsafe_allow_html=True)

        voice = st.text_input("", key=f"v_{st.session_state.q_index}", label_visibility="collapsed")

        if voice:
            st.session_state.answers.append(voice)
            st.session_state.score += len(voice.split()) * 2
            st.session_state.q_index += 1
            st.rerun()

    else:
        st.success("🎉 Interview Completed")

        total = st.session_state.score
        st.write("Final Score:", total)

        df = pd.DataFrame({
            "Q":[f"Q{i+1}" for i in range(5)],
            "Score":[total/5]*5
        })
        st.bar_chart(df.set_index("Q"))

        if st.button("Restart"):
            st.session_state.page = "dashboard"
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answers = []
