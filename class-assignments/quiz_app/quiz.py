import streamlit as st
import random

# ------------- Question Class -------------
class Question:
    def __init__(self, prompt, options, answer):
        self.prompt = prompt
        self.options = options
        self.answer = answer

    def is_correct(self, selected_option):
        return selected_option == self.answer

# ------------- Quiz Class -----------------
class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.current = 0

    def get_current_question(self):
        return self.questions[self.current]

    def check_answer(self, selected_option):
        if self.get_current_question().is_correct(selected_option):
            self.score += 1
            return True
        return False

    def next(self):
        self.current += 1

    def is_finished(self):
        return self.current >= len(self.questions)

    def restart(self):
        self.score = 0
        self.current = 0
        random.shuffle(self.questions)

# ---------- Load Questions ----------------
def load_questions():
    return [
        Question("What is the capital of France?", ["London", "Paris", "Berlin", "Madrid"], "Paris"),
        Question("What is the Python keyword for defining a function?", ["def", "function", "method", "func"], "def"),
        Question("What is 12 x 8?", ["96", "100", "108", "120"], "96"),
        Question("Which company created the iPhone?", ["Samsung", "Nokia", "Apple", "Sony"], "Apple"),
        Question("What is the largest planet in our solar system?", ["Earth", "Mars", "Jupiter", "Saturn"], "Jupiter"),
        Question("What is the chemical symbol for water?", ["O2", "H2O", "CO2", "O3"], "H2O"),
        Question("Who wrote 'Romeo and Juliet'?", ["Shakespeare", "Dickens", "Hemingway", "Austen"], "Shakespeare"),
        Question("What is the currency of Japan?", ["Yuan", "Yen", "Ringgit", "Won"], "Yen"),
        Question("What is the boiling point of water in Celsius?", ["90", "100", "110", "120"], "100"),
        Question("Who was the first President of the United States?", ["Abraham Lincoln", "George Washington", "Thomas Jefferson", "John Adams"], "George Washington"),
        Question("What is the capital of Japan?", ["Tokyo", "Kyoto", "Osaka", "Sapporo"], "Tokyo"),
        Question("Which is the largest ocean on Earth?", ["Atlantic", "Indian", "Arctic", "Pacific"], "Pacific"),
        Question("Who developed the theory of relativity?", ["Newton", "Einstein", "Bohr", "Galileo"], "Einstein"),
        Question("What is the fastest animal on land?", ["Cheetah", "Lion", "Elephant", "Horse"], "Cheetah"),
        Question("Which planet is known as the Red Planet?", ["Earth", "Mars", "Venus", "Saturn"], "Mars"),
        Question("What is the main ingredient in guacamole?", ["Tomato", "Onion", "Avocado", "Cucumber"], "Avocado"),
        Question("Which element has the chemical symbol 'O'?", ["Oxygen", "Osmium", "Ozone", "Opium"], "Oxygen"),
        Question("What is the square root of 81?", ["8", "9", "10", "11"], "9"),
        Question("Who painted the Mona Lisa?", ["Van Gogh", "Picasso", "Da Vinci", "Rembrandt"], "Da Vinci"),
        Question("What is the main language spoken in Brazil?", ["Spanish", "Portuguese", "French", "Italian"], "Portuguese")
    ]

# ----------- App Start --------------------
st.set_page_config(page_title="Quiz Game", page_icon="🧠", layout="centered")

# Night/Day Mode Toggle
if "mode" not in st.session_state:
    st.session_state.mode = "day"  # Default to day mode

def toggle_mode():
    if st.session_state.mode == "day":
        st.session_state.mode = "night"
    else:
        st.session_state.mode = "day"

# Sidebar for Night/Day Mode toggle
st.sidebar.title("Quiz Game")
st.sidebar.markdown("Test your knowledge with fun questions!")
st.sidebar.info("Created by Syed Hamza Ali Hamdani")
st.sidebar.button("🌙/🌞 Toggle Mode", on_click=toggle_mode)

# Set CSS for themes
if st.session_state.mode == "night":
    st.markdown("""
        <style>
            body {
                background-color: #1e1e1e;
                color: white;
            }
            .stButton>button {
                background-color: #444;
                color: white;
            }
            .stRadio>div>label {
                color: white;
            }
            .stTextInput input {
                color: white;
                background-color: #333;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body {
                background-color: #f0f0f0;
                color: black;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
            }
            .stRadio>div>label {
                color: black;
            }
            .stTextInput input {
                color: black;
                background-color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# Session state setup for Name and Email
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "user_info" not in st.session_state:
    st.session_state.user_info = {"name": "", "email": ""}

# Main Area - User Info Form
if st.session_state.quiz is None:
    st.title("Welcome to the Quiz Game!")
    st.markdown("Please enter your details before starting the quiz.")

    # Name and Email Input
    name = st.text_input("Enter your Name:")
    email = st.text_input("Enter your Email:")

    if st.button("Start Quiz"):
        if name and email:
            st.session_state.user_info["name"] = name
            st.session_state.user_info["email"] = email
            st.session_state.quiz = Quiz(load_questions())
            st.session_state.quiz.restart()  # Reset the quiz and start
            st.session_state.quiz.next()  # Move to the first question
        else:
            st.warning("Please enter both your name and email to start the quiz.")

# Displaying Name and Email on Left Sidebar
if st.session_state.quiz is None and st.session_state.user_info["name"]:
    st.sidebar.subheader(f"Name: {st.session_state.user_info['name']}")
    st.sidebar.subheader(f"Email: {st.session_state.user_info['email']}")

# Main Quiz Flow
if st.session_state.quiz is not None:
    quiz = st.session_state.quiz

    if not quiz.is_finished():
        q = quiz.get_current_question()
        st.subheader(f"Question {quiz.current + 1} of {len(quiz.questions)}")
        st.write(f"**{q.prompt}**")
        selected = st.radio("Choose your answer:", q.options, key=quiz.current)

        if st.button("Submit Answer"):
            correct = quiz.check_answer(selected)
            if correct:
                st.success("Correct!")
            else:
                st.error(f"Oops! Right answer is: **{q.answer}**")
            quiz.next()

    else:
        # Calculate pass/fail based on score
        total_questions = len(quiz.questions)
        percentage = (quiz.score / total_questions) * 100

        pass_fail = "Pass" if percentage >= 60 else "Fail"
        
        # Show result
        st.balloons()
        st.success(f"🎉 Congratulations {st.session_state.user_info['name']}! You completed the quiz.\n\nYour Score: **{quiz.score}/{total_questions}**")
        st.write(f"Your Email: {st.session_state.user_info['email']}")
        st.write(f"**Result: {pass_fail}** (You scored {percentage:.2f}%)")

        if st.button("Restart Quiz"):
            quiz.restart()
            st.session_state.quiz = None  # Reset the session state
            st.experimental_rerun()
