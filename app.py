import streamlit as st
import random
import time

st.set_page_config(page_title="Middle Class Pvt Ltd", layout="centered")

# ---------------- THEME TOGGLE ----------------
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

if "user" not in st.session_state:
    st.session_state.user = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    st.markdown("<h1 style='text-align:center;'>🏢 Middle Class.pvt.ltd</h1>", unsafe_allow_html=True)
    st.markdown("### 🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.session_state.user = username
            st.session_state.page = "dashboard"
        else:
            st.error("Enter valid details")

# ---------------- DASHBOARD ----------------
elif st.session_state.page == "dashboard":
    st.markdown(f"<h2>Welcome {st.session_state.user} 👋</h2>", unsafe_allow_html=True)

    st.markdown("## 📊 Job Offers")
    col1, col2 = st.columns(2)

    with col1:
        st.success("💻 Java Developer")
    with col2:
        st.info("🤖 AI Engineer")

    st.markdown("## 🧾 Resume Section")

    resume_type = st.selectbox("Select Resume Type", ["Fresher", "Experienced"])
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    # -------- FACE CHECK (SIMULATED) --------
    st.warning("⚠️ Face Verification Required (Simulation)")
    face_verified = st.checkbox("I confirm my face is visible")

    if not face_verified:
        st.error("❌ Face not detected! Access denied.")

    if uploaded_file and face_verified:
        st.success("Resume Uploaded Successfully ✅")

        if st.button("🚀 Start Interview"):
            st.session_state.page = "interview"

# ---------------- INTERVIEW ----------------
elif st.session_state.page == "interview":

    st.title("🤖 AI Interview")

    # -------- GENERATE QUESTIONS --------
    if not st.session_state.questions:
        base_questions = [
            "Explain your project.",
            "What are your strengths?",
            "Explain OOP concepts.",
            "What is your role in team?",
            "Why should we hire you?"
        ]
        st.session_state.questions = random.sample(base_questions, 5)

    q_index = len(st.session_state.answers)

    if q_index < 5:
        question = st.session_state.questions[q_index]

        st.subheader(f"Question {q_index+1}")
        st.info(question)

        # 🔊 Voice
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{question}");
        speechSynthesis.cancel();
        speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

        # 🎤 Speech-to-text
        st.markdown("""
        <button onclick="startDictation()">🎤 Speak Answer</button>
        <script>
        function startDictation() {
            var recognition = new webkitSpeechRecognition();
            recognition.lang = "en-US";

            recognition.onresult = function(event) {
                var text = event.results[0][0].transcript;
                const doc = window.parent.document;
                const area = doc.querySelector('textarea');
                if(area){
                    area.value = text;
                    area.dispatchEvent(new Event('input',{bubbles:true}));
                }
            };
            recognition.start();
        }
        </script>
        """, unsafe_allow_html=True)

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):
            if answer:
                st.session_state.answers.append(answer)
                st.rerun()
            else:
                st.warning("Please answer!")

    else:
        # -------- RESULT --------
        st.success("Interview Completed 🎉")

        scores = [min(len(a.split()) * 2, 100) for a in st.session_state.answers]
        total = sum(scores) / len(scores)

        st.write("### 📊 Overall Score:", int(total))

        st.bar_chart(scores)

        if st.button("🏠 Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.session_state.answers = []
            st.session_state.questions = []
