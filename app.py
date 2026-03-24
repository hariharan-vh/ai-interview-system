import streamlit as st
import random

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Interview System", layout="centered")

# ------------------ TITLE ------------------
st.markdown("<h1 style='text-align: center;'>🤖 AI Interview System</h1>", unsafe_allow_html=True)

# ------------------ QUESTIONS ------------------
questions = [
    "What is Artificial Intelligence?",
    "Explain Object Oriented Programming.",
    "What is a REST API?",
    "Difference between list and tuple in Python?",
    "What is Machine Learning?",
    "Explain JVM in Java.",
]

# ------------------ SESSION STATE ------------------
if "question" not in st.session_state:
    st.session_state.question = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

# ------------------ START BUTTON ------------------
if st.button("🚀 Start Interview"):
    st.session_state.question = random.choice(questions)
    st.session_state.answer = ""

# ------------------ DISPLAY QUESTION ------------------
if st.session_state.question:
    st.subheader("📌 Question:")
    st.info(st.session_state.question)

    # 🔊 TEXT TO SPEECH (VOICE OUTPUT)
    st.markdown(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{st.session_state.question}");
    msg.rate = 1;
    msg.pitch = 1;
    speechSynthesis.cancel();
    speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

    # 🎤 SPEECH TO TEXT BUTTON
    st.markdown("""
    <button onclick="startDictation()" style="
        padding:10px 20px;
        font-size:16px;
        background-color:#4CAF50;
        color:white;
        border:none;
        border-radius:5px;
        cursor:pointer;">
        🎤 Speak Answer
    </button>

    <p id="output" style="font-weight:bold; color:green;"></p>

    <script>
    function startDictation() {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = "en-US";

        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            document.getElementById("output").innerHTML = text;

            // Send to Streamlit textarea
            const streamlitDoc = window.parent.document;
            const textArea = streamlitDoc.querySelector('textarea');
            if(textArea){
                textArea.value = text;
                textArea.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };

        recognition.start();
    }
    </script>
    """, unsafe_allow_html=True)

    # ------------------ ANSWER INPUT ------------------
    answer = st.text_area("✍️ Your Answer (voice will appear here):")

    # ------------------ SUBMIT ------------------
    if st.button("✅ Submit Answer"):
        if answer.strip() == "":
            st.warning("Please speak or type your answer!")
        else:
            st.success("Answer Submitted Successfully ✅")

            # ------------------ SIMPLE EVALUATION ------------------
            score = min(len(answer.split()) * 2, 100)

            st.subheader("📊 Evaluation Result")
            st.write(f"**Score:** {score}/100")

            if score > 70:
                st.success("Excellent Answer 🎉")
            elif score > 40:
                st.info("Good Answer 👍")
            else:
                st.error("Needs Improvement ❗")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("<center>💼 AI Interview System | Resume Project Ready</center>", unsafe_allow_html=True)
