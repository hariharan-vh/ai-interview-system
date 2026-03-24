import streamlit as st
import random
import time

st.set_page_config(page_title="Middle Class Pvt Ltd", layout="centered")

# ---------------- THEME ----------------
theme = st.sidebar.selectbox("🌗 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
        body { background-color: #0E1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------------- LOGIN ----------------
if st.session_state.page == "login":
    st.markdown("<h1 style='text-align:center;'>🏢 Middle Class.pvt.ltd</h1>", unsafe_allow_html=True)
    st.markdown("## 🔐 Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user and pwd:
            st.session_state.page = "dashboard"
        else:
            st.error("Enter valid details")

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":
    st.title("📊 Dashboard")

    st.success("💼 Job Roles: AI Engineer | Java Developer")

    resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    # CAMERA (FACE PRESENCE)
    st.markdown("### 🎥 Face Check")

    st.markdown("""
    <video id="video" width="300" autoplay></video>
    <p id="status">Checking camera...</p>

    <script>
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        document.getElementById('video').srcObject = stream;
        document.getElementById("status").innerHTML = "✅ Camera Active (Face assumed)";
    })
    .catch(function(err) {
        document.getElementById("status").innerHTML = "❌ Camera Blocked";
    });
    </script>
    """, unsafe_allow_html=True)

    if resume:
        if st.button("🚀 Start Interview"):
            st.session_state.page = "interview"

# ---------------- INTERVIEW ----------------
elif st.session_state.page == "interview":

    st.title("🤖 AI Voice Interview")

    if not st.session_state.questions:
        qlist = [
            "Tell me about yourself",
            "Explain your project",
            "What are your strengths",
            "Why should we hire you",
            "Explain your technical skills"
        ]
        st.session_state.questions = random.sample(qlist, 5)

    index = len(st.session_state.answers)

    if index < 5:
        question = st.session_state.questions[index]

        st.subheader(f"Question {index+1}")
        st.info(question)

        # 🔊 FEMALE VOICE
        st.markdown(f"""
        <script>
        function speakQuestion() {{
            var msg = new SpeechSynthesisUtterance("{question}");
            var voices = speechSynthesis.getVoices();

            // Try to pick female voice
            for (let i = 0; i < voices.length; i++) {{
                if (voices[i].name.toLowerCase().includes("female") || voices[i].name.includes("Google UK English Female")) {{
                    msg.voice = voices[i];
                    break;
                }}
            }}

            msg.rate = 1;
            msg.pitch = 1.2;
            speechSynthesis.cancel();
            speechSynthesis.speak(msg);
        }}
        speakQuestion();
        </script>
        """, unsafe_allow_html=True)

        # ⏱️ TIMER
        st.write("⏳ Thinking Time: 30 seconds")
        timer = st.empty()

        for i in range(30, 0, -1):
            timer.write(f"{i} sec remaining...")
            time.sleep(1)

        st.success("🎤 Speak your answer now")

        # 🎤 SPEECH TO TEXT (AUTO SUBMIT)
        st.markdown(f"""
        <button onclick="startVoice()">🎤 Start Speaking</button>
        <p id="result"></p>

        <script>
        function startVoice() {{
            var recognition = new webkitSpeechRecognition();
            recognition.lang = "en-US";
            recognition.continuous = false;

            recognition.onresult = function(event) {{
                var text = event.results[0][0].transcript;
                document.getElementById("result").innerHTML = "✅ " + text;

                // Send answer to Streamlit via query params
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    value: text
                }}, "*");
            }};

            recognition.start();
        }}
        </script>
        """, unsafe_allow_html=True)

        # HIDDEN INPUT CAPTURE
        spoken_text = st.text_input("voice_input", key=f"voice_{index}")

        if spoken_text:
            st.session_state.answers.append(spoken_text)
            st.rerun()

    else:
        # RESULT
        st.success("🎉 Interview Completed")

        scores = [min(len(a.split()) * 2, 100) for a in st.session_state.answers]
        total = int(sum(scores) / len(scores))

        st.write("## 📊 Overall Score:", total)
        st.bar_chart(scores)

        if st.button("🏠 Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.session_state.answers = []
            st.session_state.questions = []
