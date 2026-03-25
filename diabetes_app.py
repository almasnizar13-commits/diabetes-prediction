import streamlit as st
import sqlite3
import pandas as pd
import pickle
from datetime import datetime
import numpy as np

# ---------------- CSS ----------------
st.markdown("""
<style>
.main {background-color: #f5f7fa;}
h1, h2, h3 {color: #2c3e50;}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    padding: 10px;
    font-weight: bold;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DB ----------------
conn = sqlite3.connect("diabetes.db", check_same_thread=False)
c = conn.cursor()

def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    gender TEXT,
                    glucose REAL,
                    bp REAL,
                    insulin REAL,
                    bmi REAL,
                    result TEXT,
                    probability REAL,
                    recommendation TEXT,
                    date TEXT)''')
    conn.commit()

create_tables()

# ---------------- AUTH ----------------
def add_user(u, p):
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
    conn.commit()

def login_user(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    return c.fetchone()

# ---------------- DATA ----------------
def add_record(data):
    c.execute('''INSERT INTO records
                 (name, age, gender, glucose, bp, insulin, bmi,
                  result, probability, recommendation, date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()

def view_records():
    c.execute("SELECT * FROM records")
    return c.fetchall()

# ---------------- MODEL ----------------
model = pickle.load(open("diabetes_svm_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- RECOMMENDATION ----------------
def get_recommendation(prob):
    if prob >= 70:
        return "HIGH RISK: Consult doctor, strict diet, daily exercise"
    elif prob >= 40:
        return "MODERATE RISK: Control diet, exercise regularly"
    else:
        return "LOW RISK: Maintain healthy lifestyle"

# ---------------- LOGIN ----------------
def login_page():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("🔐 Login")

    menu = ["Login", "Signup"]
    choice = st.selectbox("Option", menu)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.login = True
                st.success("Login Successful")
            else:
                st.error("Invalid Credentials")
    else:
        if st.button("Create Account"):
            add_user(username, password)
            st.success("Account Created")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN ----------------
def main_app():
    st.sidebar.title("Menu")
    choice = st.sidebar.selectbox("Select", ["Prediction", "History", "Logout"])

    # -------- PREDICTION --------
    if choice == "Prediction":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.title("🩺 Diabetes Prediction")

        name = st.text_input("Name")
        age = st.number_input("Age", 1, 120)
        gender = st.selectbox("Gender", ["Male", "Female"])

        glucose = st.number_input("Glucose")
        bp = st.number_input("Blood Pressure")
        insulin = st.number_input("Insulin")
        bmi = st.number_input("BMI")

        if st.button("Predict"):

            # -------- VALIDATION --------
            if glucose <= 0 or bp <= 0 or insulin <= 0 or bmi <= 0:
                st.error("❌ Enter valid medical values")
                st.stop()

            # -------- FEATURE --------
            features = np.array([[glucose, bp, insulin, bmi]])

            # -------- SCALING --------
            features_scaled = scaler.transform(features)

            # -------- PREDICTION --------
            result = model.predict(features_scaled)[0]
            prob = round(model.predict_proba(features_scaled)[0][1] * 100, 2)

            result_text = "Diabetic" if result == 1 else "Non-Diabetic"
            recommendation = get_recommendation(prob)

            # -------- SAVE --------
            add_record((name, age, gender, glucose, bp, insulin, bmi,
                        result_text, prob, recommendation, str(datetime.now())))

            # -------- RESULT --------
            if result == 1:
                st.error(f"🔴 High Risk ({prob}%)")
            else:
                st.success(f"🟢 Low Risk ({prob}%)")

            st.markdown("### 🩺 Recommendation")
            st.info(recommendation)

            # -------- VISUALIZATION --------
            df = pd.DataFrame({
                "Parameter": ["Glucose", "BP", "Insulin", "BMI"],
                "Value": [glucose, bp, insulin, bmi]
            })
            st.bar_chart(df.set_index("Parameter"))

        st.markdown("</div>", unsafe_allow_html=True)

    # -------- HISTORY --------
    elif choice == "History":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.title("📂 History")

        data = view_records()

        df = pd.DataFrame(data, columns=[
            "ID","Name","Age","Gender","Glucose","BP","Insulin","BMI",
            "Result","Probability","Recommendation","Date"
        ])

        st.dataframe(df)

        # -------- FILTER --------
        filter_option = st.selectbox("Filter", ["All", "High Risk Only"])

        if filter_option == "High Risk Only":
            df = df[df["Probability"] > 70]

        # -------- CSV DOWNLOAD --------
        csv = df.to_csv(index=False)

        st.download_button(
            "⬇ Download CSV",
            csv,
            "report.csv",
            "text/csv"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    elif choice == "Logout":
        st.session_state.login = False

# ---------------- FLOW ----------------
if st.session_state.login:
    main_app()
else:
    login_page()
