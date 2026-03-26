import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import pickle
import hashlib
from datetime import datetime
import plotly.express as px
from fpdf import FPDF

# =========================
# CONFIG + CSS
# =========================
st.set_page_config(layout="wide")

st.markdown("""
<style>
body {background-color:#0e1117; color:white;}
.block-container {padding:2rem;}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model = pickle.load(open("diabetes_svm_model.pkl","rb"))
scaler = pickle.load(open("scaler.pkl","rb"))

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("diabetes.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS patients(username TEXT, patient_id TEXT, name TEXT, age INT, gender TEXT)")
c.execute("""CREATE TABLE IF NOT EXISTS records(
    username TEXT, patient_id TEXT, date TEXT,
    glucose REAL, bmi REAL, bp REAL, insulin REAL,
    result TEXT, prob REAL, risk TEXT)""")
conn.commit()

# =========================
# AUTH
# =========================
def hash_pass(p):
    return hashlib.sha256(p.encode()).hexdigest()

def login(u,p):
    return c.execute("SELECT * FROM users WHERE username=? AND password=?",
                     (u,hash_pass(p))).fetchone()

def register(u,p):
    c.execute("INSERT INTO users VALUES (?,?,?)",(u,hash_pass(p),"user"))
    conn.commit()

# =========================
# HELPERS
# =========================
def get_risk(prob):
    if prob > 0.7: return "HIGH"
    elif prob > 0.4: return "MEDIUM"
    return "LOW"

def generate_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for _,row in df.iterrows():
        pdf.cell(0,8,f"{row['patient_id']} | {row['result']} | {row['risk']}",ln=True)

    out = pdf.output(dest='S')
    return out if isinstance(out, bytes) else out.encode('latin1')

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# =========================
# LOGIN PAGE
# =========================
def login_page():
    st.title("Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        data = login(u,p)
        if data:
            st.session_state.user = data[0]
            st.session_state.role = data[2]
            st.rerun()
        else:
            st.error("Wrong credentials")

    if st.button("Register"):
        register(u,p)
        st.success("Account created")

# =========================
# ADD PATIENT
# =========================
def patient_page():
    st.subheader("Add Patient")

    pid = st.text_input("Patient ID")
    name = st.text_input("Name")
    age = st.number_input("Age",1,120)
    gender = st.selectbox("Gender",["Male","Female"])

    if st.button("Save"):
        c.execute("INSERT INTO patients VALUES (?,?,?,?,?)",
                  (st.session_state.user,pid,name,age,gender))
        conn.commit()
        st.success("Saved")

# =========================
# PREDICTION
# =========================
def prediction_page():
    df = pd.read_sql(f"SELECT * FROM patients WHERE username='{st.session_state.user}'",conn)

    if df.empty:
        st.warning("Add patient first")
        return

    pid = st.selectbox("Patient", df["patient_id"])

    glucose = st.slider("Glucose",0,200)
    bmi = st.slider("BMI",10.0,50.0)
    bp = st.slider("BP",0,150)
    insulin = st.slider("Insulin",0,300)

    if st.button("Predict"):
        data = scaler.transform([[glucose,bmi,bp,insulin]])
        pred = model.predict(data)[0]
        prob = abs(model.decision_function(data)[0])

        res = "Diabetic" if pred else "Non-Diabetic"
        risk = get_risk(prob)

        st.success(f"{res} | {risk}")

        c.execute("INSERT INTO records VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (st.session_state.user,pid,datetime.now(),
                   glucose,bmi,bp,insulin,res,prob,risk))
        conn.commit()

# =========================
# DASHBOARD
# =========================
def dashboard_page():
    df = pd.read_sql(f"SELECT * FROM records WHERE username='{st.session_state.user}'",conn)

    if df.empty:
        st.info("No data")
        return

    col1,col2 = st.columns(2)

    col1.plotly_chart(px.pie(df,names="risk",title="Risk Distribution"))
    col2.plotly_chart(px.histogram(df,x="glucose",title="Glucose"))

    st.plotly_chart(px.scatter(df,x="bmi",y="glucose",color="risk"))

# =========================
# RECORDS
# =========================
def records_page():
    df = pd.read_sql(f"SELECT * FROM records WHERE username='{st.session_state.user}'",conn)

    st.dataframe(df)

    csv = df.to_csv(index=False).encode()
    st.download_button("CSV",csv)

    pdf = generate_pdf(df)
    st.download_button("PDF",pdf)

# =========================
# ADMIN
# =========================
def admin_page():
    st.title("Admin Panel")

    df = pd.read_sql("SELECT * FROM records",conn)

    st.metric("Total Records", len(df))
    st.metric("Diabetic", len(df[df['result']=="Diabetic"]))

    st.plotly_chart(px.box(df,y="bmi"))

# =========================
# MAIN ROUTER
# =========================
if not st.session_state.user:
    login_page()

else:
    role = st.session_state.role

    if role == "admin":
        menu = st.sidebar.radio("Menu",["Admin","Logout"])
    else:
        menu = st.sidebar.radio("Menu",
            ["Patient","Prediction","Dashboard","Records","Logout"])

    if menu == "Patient": patient_page()
    elif menu == "Prediction": prediction_page()
    elif menu == "Dashboard": dashboard_page()
    elif menu == "Records": records_page()
    elif menu == "Admin": admin_page()
    elif menu == "Logout":
        st.session_state.user = None
        st.rerun()
