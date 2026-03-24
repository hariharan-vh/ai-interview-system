import streamlit as st
import random

st.set_page_config(page_title="Middle Class Pvt Ltd", layout="centered")

# ---------------- THEME ----------------
theme = st.sidebar.selectbox("🌗 Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown("""
        <style>
        .stApp {background:#0e1117; color:white;}
        .card {background:#1c1f26; padding:20px; border-radius:12px;}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .card {background:#f5f5f5; padding:20px; border-radius:12px;}
        </style>
    """, unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "skills" not in st.session_state:
    st.session_state.skills = []

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

    st.markdown("### 💼 Job Offers")
    st.success("💻 Java Developer")
    st.info("🤖 AI Engineer")

    # Resume
    file = st.file_uploader("📄 Upload Resume", type=["txt"])

    if file:
        text = file.read().decode("utf-8").lower()

        skills_db = ["python","java","ai","ml","sql","data","web"]
        st.session_state.skills = [s for s in skills_db if s in text]

        st.success("Resume Processed ✅")
        st.write("Skills:", st.session_state.skills)

        if st.button("🚀 Start Interview"):
            st.session_state.page = "interview"

# ---------------- INTERVIEW ----------------
elif st.session_state.page == "interview":

    st.title("🤖 AI Voice Interview")

    # Generate Questions
    if not st.session_state.questions:
        base = [
            "Tell me about yourself",
            "Explain your project",
            "What are your strengths",
            "Why should we hire you",
            "Explain your technical skills"
        ]

        if st.session_state.skills:
            st.session_state.questions = [f"Explain {s}" for s in st.session_state.skills[:5]]
        else:
            st.session_state.questions = random.sample(base, 5)

    index = len(st.session_state.answers)

    if index < 5:
        q = st.session_state.questions[index]

        st.markdown(f"<div class='card'>🤖 {q}</div>", unsafe_allow_html=True)

        # 🔊 FEMALE VOICE
        st.markdown(f"""
        <script>
        function speak() {{
            var msg = new SpeechSynthesisUtterance("{q}");
            var voices = speechSynthesis.getVoices();

            for (let i=0; i<voices.length; i++) {{
                if (voices[i].name.includes("Female") || voices[i].name.includes("Google UK English Female")) {{
                    msg.voice = voices[i];
                    break;
                }}
            }}

            msg.pitch = 1.2;
            msg.rate = 1;
            speechSynthesis.cancel();
            speechSynthesis.speak(msg);
        }}
        speak();
        </script>
        """, unsafe_allow_html=True)

        # ⏱️ TIMER (visual only)
        st.markdown("⏳ **Think for 30 seconds before answering...**")

        # 🎤 SPEECH TO TEXT (WORKING)
        st.markdown(f"""
        <button onclick="startSpeech()">🎤 Speak Answer</button>
        <p id="status"></p>

        <script>
        function startSpeech() {{
            var recognition = new webkitSpeechRecognition();
            recognition.lang = "en-US";

            recognition.onstart = function() {{
                document.getElementById("status").innerHTML = "🎙️ Listening...";
            }};

            recognition.onresult = function(event) {{
                var text = event.results[0][0].transcript;
                document.getElementById("status").innerHTML = "✅ " + text;

                const streamlitDoc = window.parent.document;
                const input = streamlitDoc.querySelector('input[type="text"]');
                if(input){{
                    input.value = text;
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }};

            recognition.start();
        }}
        </script>
        """, unsafe_allow_html=True)

        # Hidden capture
        voice_input = st.text_input("voice", key=f"v_{index}")

        if voice_input:
            st.session_state.answers.append(voice_input)
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
