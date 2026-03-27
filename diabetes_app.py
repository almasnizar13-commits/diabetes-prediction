import streamlit as st
import sqlite3, hashlib, os, pickle, numpy as np, pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import plotly.express as px

# ---------------- Setup ----------------
st.set_page_config(page_title="Diabetes Prediction System", layout="wide")

# Embedded CSS
st.markdown("""
<style>
body {
    background-image: url("https://images.unsplash.com/photo-1576091160399-112ba8d25d02?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #333;
}
.stApp {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
h1, h2, h3, h4, h5, h6 { color: #0056b3; }
.stButton>button {
    background-color: #007bff;
    color: white;
    border-radius: 5px;
    padding: 8px 15px;
    border: none;
}
.stButton>button:hover { background-color: #0056b3; }
</style>
""", unsafe_allow_html=True)

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
            bmi REAL, dpf REAL, history TEXT,
            prediction TEXT, date TEXT
            )""")
conn.commit()

# ---------------- Helper Functions ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    try:
        c.execute("INSERT INTO users (username,password) VALUES (?,?)", 
                  (username, hash_password(password)))
        conn.commit()
    except:
        st.error("Username already exists")

def check_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", 
              (username, hash_password(password)))
    return c.fetchone()

# Load ML model and scaler
model = pickle.load(open("diabetes_svm_model.pkl","rb"))
scaler = pickle.load(open("scaler.pkl","rb"))

def predict_diabetes(data):
    data_scaled = scaler.transform([data])
    pred = model.predict(data_scaled)
    return "Diabetic" if pred[0]==1 else "Non-Diabetic"

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
    c_pdf.drawString(100,590,f"Medical History: {patient['history']}")
    c_pdf.drawString(100,570,f"Prediction: {patient['prediction']}")
    c_pdf.drawString(100,550,"Health Tips:")
    y = 530
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
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.subheader("New User? Register")
    new_username = st.text_input("New Username", key="new_username")
    new_password = st.text_input("New Password", type="password", key="new_password")
    if st.button("Register"):
        add_user(new_username, new_password)
        st.success("User created! Please login.")

# ---------------- Dashboard ----------------
if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    menu = st.sidebar.selectbox("Menu", ["Add Patient","View Patients","Logout"])
    
    if menu=="Logout":
        st.session_state.logged_in = False
        st.rerun()

    # ---------------- Add Patient ----------------
    if menu=="Add Patient":
        st.subheader("Add Patient Details")
with st.form("patient_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    # ... other inputs ...
    submitted = st.form_submit_button("Predict & Save")

if submitted:
    # Process prediction
    patient_data = [glucose, bp, insulin, bmi, dpf, age]
    prediction = predict_diabetes(patient_data)
    tips = health_tips(prediction)
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save to DB
    c.execute("""INSERT INTO patients 
                 (name, age, gender, glucose, bp, insulin, bmi, dpf, history, prediction, date)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
              (name, age, gender, glucose, bp, insulin, bmi, dpf, history, prediction, date))
    conn.commit()
    patient_id = c.lastrowid

    # Generate PDF
    patient_dict = {"id": patient_id, "name": name, "age": age, "gender": gender,
                    "glucose": glucose, "bp": bp, "insulin": insulin, "bmi": bmi, "dpf": dpf,
                    "history": history, "prediction": prediction, "tips": tips}
    pdf_file = generate_pdf(patient_dict)

    # Show results outside the form
    st.success(f"Patient saved. Prediction: {prediction}")

    # Download button must be **outside the form**
    with open(pdf_file, "rb") as file:
        st.download_button("Download PDF Report", file.read(), file_name=f"{name}_{patient_id}.pdf", mime="application/pdf")

    # ---------------- View Patients ----------------
    if menu=="View Patients":
        st.subheader("All Patients Records")
        df = pd.read_sql("SELECT * FROM patients", conn)
        if not df.empty:
            st.dataframe(df)
            st.download_button("Download All Records CSV", df.to_csv(index=False).encode('utf-8'), file_name="all_patients.csv", mime="text/csv")
            
            st.subheader("Glucose Distribution")
            fig = px.histogram(df, x="glucose", nbins=20, title="Glucose Level Distribution")
            st.plotly_chart(fig)

            st.subheader("Prediction Outcome Distribution")
            outcome_counts = df['prediction'].value_counts().reset_index()
            outcome_counts.columns = ['Outcome', 'Count']
            fig_outcome = px.bar(outcome_counts, x='Outcome', y='Count',
                                 title='Diabetes Prediction Outcomes',
                                 color='Outcome',
                                 color_discrete_map={'Diabetic': 'red', 'Non-Diabetic': 'green'})
            st.plotly_chart(fig_outcome)

            st.subheader("Patient Specific Details")
            patient_names = df['name'].unique()
            selected_name = st.selectbox("Select Patient to view details:", patient_names)
            if selected_name:
                selected_patient_df = df[df['name']==selected_name].iloc[0]
                st.write(f"**Name:** {selected_patient_df['name']}")
                st.write(f"**Age:** {selected_patient_df['age']}")
                st.write(f"**Gender:** {selected_patient_df['gender']}")
                st.write(f"**Prediction:** {selected_patient_df['prediction']}")
                st.markdown(f"**Medical History:** {selected_patient_df['history']}")
                st.markdown(f"**Date Recorded:** {selected_patient_df['date']}")

                patient_dict_for_pdf = {
                    "id": selected_patient_df['id'],
                    "name": selected_patient_df['name'],
                    "age": selected_patient_df['age'],
                    "gender": selected_patient_df['gender'],
                    "glucose": selected_patient_df['glucose'],
                    "bp": selected_patient_df['bp'],
                    "insulin": selected_patient_df['insulin'],
                    "bmi": selected_patient_df['bmi'],
                    "dpf": selected_patient_df['dpf'],
                    "history": selected_patient_df['history'],
                    "prediction": selected_patient_df['prediction'],
                    "tips": health_tips(selected_patient_df['prediction'])
                }
                pdf_file_selected = generate_pdf(patient_dict_for_pdf)
                with open(pdf_file_selected, "rb") as file:
                    st.download_button(
                        "Download PDF for Selected Patient",
                        file.read(),
                        file_name=f"{selected_patient_df['name']}_{selected_patient_df['id']}.pdf",
                        mime="application/pdf"
                    )
        else:
            st.info("No patient records found yet.")
