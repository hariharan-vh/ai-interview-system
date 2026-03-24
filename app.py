import streamlit as st
import random
import pandas as pd
import time

st.set_page_config(page_title="AI Interview", layout="wide")

# ---------------- THEME ----------------
if st.sidebar.toggle("🌗 Dark Mode"):
    st.markdown("<style>.stApp{background:#0e1117;color:white;}</style>", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
with col2:
    st.markdown("<h1>MIDDLE CLASS.pvt.ltd.</h1>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
for k,v in {
    "started":False,
    "q_index":0,
    "score":0,
    "answers":[]
}.items():
    if k not in st.session_state:
        st.session_state[k]=v

# ---------------- QUESTIONS ----------------
questions = [
    "What is Artificial Intelligence?",
    "Explain your project",
    "What are your strengths?",
    "Why should we hire you?",
    "Explain your technical skills"
]

# ---------------- START ----------------
st.subheader("🎭 AI Interview")

if not st.session_state.started:
    if st.button("Start Interview 🚀"):
        st.session_state.started = True

# ---------------- INTERVIEW ----------------
if st.session_state.started and st.session_state.q_index < len(questions):

    q = questions[st.session_state.q_index]

    # ---------------- QUESTION UI ----------------
    st.markdown(f"<div style='padding:15px;border-radius:10px;background:#f1f1f1;'>🤖 {q}</div>", unsafe_allow_html=True)

    # ---------------- AI VOICE ----------------
    st.markdown(f"""
    <script>
    function speakQuestion(){{
        var msg = new SpeechSynthesisUtterance("{q}");
        var voices = speechSynthesis.getVoices();

        for (let i=0; i<voices.length; i++){{
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
    speakQuestion();
    </script>
    """, unsafe_allow_html=True)

    # ---------------- ROBOT IMAGE ----------------
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)

    # ---------------- TIMER ----------------
    timer = st.empty()
    for i in range(30,0,-1):
        timer.info(f"⏳ Thinking Time: {i}s")
        time.sleep(1)

    st.success("🎤 Speak Now")

    # ---------------- SPEECH ONLY ----------------
    st.markdown("""
    <button onclick="startSpeech()" style="padding:10px 20px;font-size:16px;">
    🎤 Speak Answer
    </button>

    <p id="output"></p>

    <script>
    function startSpeech() {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            document.getElementById("output").innerHTML = "✅ " + text;

            const doc = window.parent.document;
            const input = doc.querySelector('input[type="text"]');
            if(input){
                input.value = text;
                input.dispatchEvent(new Event('input', {bubbles:true}));
            }
        };

        recognition.start();
    }
    </script>
    """, unsafe_allow_html=True)

    # HIDDEN FIELD (no typing UI)
    voice = st.text_input("", key=f"voice_{st.session_state.q_index}", label_visibility="collapsed")

    # AUTO SUBMIT
    if voice:
        st.session_state.answers.append(voice)

        score = min(len(voice.split()) * 2, 100)
        st.session_state.score += score

        st.session_state.q_index += 1
        st.rerun()

# ---------------- RESULT ----------------
elif st.session_state.q_index >= len(questions):

    st.success("🎉 Interview Completed")

    total = st.session_state.score
    st.write("## 📊 Final Score:", total)

    df = pd.DataFrame({
        "Questions":[f"Q{i+1}" for i in range(5)],
        "Score":[total/5]*5
    })

    st.bar_chart(df.set_index("Questions"))

    if st.button("Restart"):
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.started = False
