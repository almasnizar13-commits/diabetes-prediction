import streamlit as st
import sqlite3, hashlib, os, pickle, numpy as np, pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import plotly.express as px



body {
    background-color: #f9f9f9;
    font-family: 'Arial', sans-serif;
}

h1, h2, h3 {
    color: #2F4F4F;
}

.stButton button {
    background-color: #4CAF50;
    color: white;
    padding: 8px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.stButton button:hover {
    background-color: #45a049;
}

.stTextInput>div>input {
    border-radius: 5px;
    border: 1px solid #ccc;
    padding: 5px;
}
# ---------------- Setup ----------------
st.set_page_config(page_title="Diabetes Prediction System", layout="wide")
st.markdown('<link rel="stylesheet" href="static/style.css">', unsafe_allow_html=True)

os.makedirs("reports", exist_ok=True)
os.makedirs("database", exist_ok=True)

# ---------------- Database ----------------
conn = sqlite3.connect("database/patients.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
            )""")

c.execute("""CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, age INTEGER, gender TEXT,
            glucose REAL, bp REAL, insulin REAL,
            bmi REAL, dpf REAL, risk_factors TEXT,
            history TEXT, prediction TEXT, date TEXT
            )""")
conn.commit()

# ---------------- Helper Functions ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    try:
        c.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, hash_password(password)))
        conn.commit()
    except:
        st.error("Username already exists")

def check_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return c.fetchone()

# Load ML model and scaler
model = pickle.load(open("model/diabetes_svm_model.pkl","rb"))
scaler = pickle.load(open("model/scaler.pkl","rb"))

def predict_diabetes(data):
    data_scaled = scaler.transform([data])
    prediction = model.predict(data_scaled)
    return "Diabetic" if prediction[0]==1 else "Non-Diabetic"

def health_tips(prediction):
    if prediction=="Diabetic":
        return ["Monitor sugar daily", "Exercise 30 min/day", "Avoid sugary food"]
    else:
        return ["Maintain healthy diet", "Regular check-ups", "Exercise regularly"]

def generate_pdf(patient):
    filename = f"reports/{patient['name']}_{patient['id']}.pdf"
    c_pdf = canvas.Canvas(filename, pagesize=letter)
    c_pdf.drawString(100,750,f"Patient Name: {patient['name']}")
    c_pdf.drawString(100,730,f"Age: {patient['age']}")
    c_pdf.drawString(100,710,f"Gender: {patient['gender']}")
    c_pdf.drawString(100,690,f"Glucose: {patient['glucose']}")
    c_pdf.drawString(100,670,f"BP: {patient['bp']}")
    c_pdf.drawString(100,650,f"Insulin: {patient['insulin']}")
    c_pdf.drawString(100,630,f"BMI: {patient['bmi']}")
    c_pdf.drawString(100,610,f"DPF: {patient['dpf']}")
    c_pdf.drawString(100,590,f"Risk Factors: {patient['risk_factors']}")
    c_pdf.drawString(100,570,f"History: {patient['history']}")
    c_pdf.drawString(100,550,f"Prediction: {patient['prediction']}")
    c_pdf.drawString(100,530,"Health Tips:")
    y = 510
    for tip in patient['tips']:
        c_pdf.drawString(120, y, f"- {tip}")
        y -= 20
    c_pdf.save()
    return filename

# ---------------- Session State ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

st.title("Diabetes Prediction System")

# ---------------- Login ----------------
if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = check_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid username or password")
    st.subheader("New User? Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        add_user(new_username, new_password)
        st.success("User created! Please login.")

# ---------------- Dashboard ----------------
if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    menu = st.sidebar.selectbox("Menu", ["Add Patient","View Patients","Logout"])
    
    if menu=="Logout":
        st.session_state.logged_in = False
        st.experimental_rerun()

    # ---------------- Add Patient ----------------
    if menu=="Add Patient":
        st.subheader("Add Patient Details")
        with st.form("patient_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0, max_value=120)
            gender = st.selectbox("Gender", ["Male","Female","Other"])
            glucose = st.number_input("Glucose")
            bp = st.number_input("Blood Pressure")
            insulin = st.number_input("Insulin")
            bmi = st.number_input("BMI")
            dpf = st.number_input("DPF")
            risk_factors = st.text_area("Risk Factors")
            history = st.text_area("History")
            submitted = st.form_submit_button("Predict & Save")
            if submitted:
                patient_data = [glucose,bp,insulin,bmi,dpf,age]
                prediction = predict_diabetes(patient_data)
                tips = health_tips(prediction)
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("""INSERT INTO patients (name, age, gender, glucose, bp, insulin, bmi, dpf, risk_factors, history, prediction, date)
                             VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                             (name, age, gender, glucose, bp, insulin, bmi, dpf, risk_factors, history, prediction, date))
                conn.commit()
                patient_id = c.lastrowid
                patient_dict = {"id": patient_id, "name": name, "age": age, "gender": gender,
                                "glucose": glucose, "bp": bp, "insulin": insulin, "bmi": bmi, "dpf": dpf,
                                "risk_factors": risk_factors, "history": history, "prediction": prediction, "tips": tips}
                pdf_file = generate_pdf(patient_dict)
                st.success(f"Patient saved. Prediction: {prediction}")
                st.download_button("Download PDF Report", pdf_file, file_name=f"{name}_{patient_id}.pdf")

    # ---------------- View Patients ----------------
    if menu=="View Patients":
        st.subheader("All Patients Records")
        df = pd.read_sql("SELECT * FROM patients", conn)
        if not df.empty:
            st.dataframe(df)
            st.download_button("Download All Records CSV", df.to_csv(index=False), file_name="all_patients.csv")
            
            st.subheader("Glucose Distribution")
            fig = px.histogram(df, x="glucose", nbins=20, title="Glucose Level Distribution")
            st.plotly_chart(fig)
