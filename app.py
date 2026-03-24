import streamlit as st
import random
import time

st.set_page_config(page_title="Middle Class Pvt Ltd", layout="centered")

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
    st.success("💼 Job Roles Available: AI Engineer | Java Developer")

    resume_type = st.selectbox("Resume Type", ["Fresher", "Experienced"])
    resume = st.file_uploader("Upload Resume", type=["pdf"])

    # ---------- FACE DETECTION ----------
    st.markdown("### 🎥 Face Verification")

    st.markdown("""
    <video id="video" width="300" autoplay></video>
    <p id="face_status">Checking face...</p>

    <script>
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        document.getElementById('video').srcObject = stream;
        document.getElementById("face_status").innerHTML = "✅ Face detected (Camera Active)";
    })
    .catch(function(err) {
        document.getElementById("face_status").innerHTML = "❌ No face detected / Camera blocked";
    });
    </script>
    """, unsafe_allow_html=True)

    if resume:
        if st.button("🚀 Start Interview"):
            st.session_state.page = "interview"

# ---------------- INTERVIEW ----------------
elif st.session_state.page == "interview":

    st.title("🤖 AI Voice Interview")

    # generate questions
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

        # 🔊 VOICE QUESTION
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{question}");
        speechSynthesis.cancel();
        speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

        # ⏱️ THINKING TIMER
        st.write("⏳ Thinking Time: 30 seconds")
        timer_placeholder = st.empty()

        for i in range(30, 0, -1):
            timer_placeholder.write(f"Time left: {i} sec")
            time.sleep(1)

        st.success("🎤 Start Speaking Now!")

        # 🎤 SPEECH TO TEXT
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

        answer = st.text_area("Your Answer (auto voice input)")

        if st.button("Submit Answer"):
            if answer:
                st.session_state.answers.append(answer)
                st.rerun()
            else:
                st.warning("Please speak your answer!")

    else:
        # -------- RESULT --------
        st.success("🎉 Interview Completed")

        scores = [min(len(a.split()) * 2, 100) for a in st.session_state.answers]
        total = int(sum(scores) / len(scores))

        st.write("## 📊 Overall Score:", total)
        st.bar_chart(scores)

        if st.button("🏠 Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.session_state.answers = []
            st.session_state.questions = []
