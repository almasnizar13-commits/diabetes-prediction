import streamlit as st
import numpy as np
import pickle
import pandas as pd
from datetime import datetime

model  = pickle.load(open("diabetes_rf_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.set_page_config(
    page_title="Diabetes Prediction — Smart Health System",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(135deg, #0d1b2a 0%, #1a3a4a 100%); }

h1,h2,h3,h4,h5,h6 { color: #ffffff !important; }
p  { color: rgba(255,255,255,0.85) !important; }
li { color: rgba(255,255,255,0.80) !important; }

label {
    color: #ffffff !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

.stNumberInput input,
.stTextInput input {
    background: #ffffff !important;
    color: #000000 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border: 2px solid #0a9396 !important;
    border-radius: 8px !important;
}

.stTextArea textarea {
    background: #ffffff !important;
    color: #000000 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border: 2px solid #0a9396 !important;
    border-radius: 8px !important;
}

/* ✅ SELECT BOX FIX */
.stSelectbox div[data-baseweb="select"] {
    background: #ffffff !important;
    border: 2px solid #0a9396 !important;
    border-radius: 8px !important;
}
.stSelectbox div[data-baseweb="select"] span {
    color: #000000 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
}
.stSelectbox div[data-baseweb="select"] div {
    color: #000000 !important;
    background: #ffffff !important;
}
.stSelectbox svg { fill: #000000 !important; }
[data-baseweb="popover"] { background: #ffffff !important; }
[data-baseweb="popover"] li {
    color: #000000 !important;
    background: #ffffff !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-baseweb="popover"] li:hover {
    background: #e6f9f9 !important;
    color: #005f73 !important;
}
[data-baseweb="menu"] { background: #ffffff !important; }
[data-baseweb="menu"] li {
    color: #000000 !important;
    font-size: 14px !important;
}
[data-baseweb="menu"] li:hover { background: #e6f9f9 !important; }
[data-baseweb="select"] input { color: #000000 !important; }

.header-box {
    background: linear-gradient(135deg, #0a9396, #005f73);
    border-radius: 16px; padding: 28px 36px;
    text-align: center; margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.header-box h1 { color: white !important; font-size: 28px; font-weight: 700; margin:0; }
.header-box p  { color: rgba(255,255,255,0.85) !important; font-size: 13px; margin:6px 0 0; }

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px; padding: 24px; margin-bottom: 16px;
}
.card h4 {
    color: #94d2bd !important; margin-bottom: 16px;
    font-size:16px; border-bottom:1px solid rgba(255,255,255,0.1);
    padding-bottom:8px;
}

.login-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px; padding: 44px 40px;
    max-width: 420px; margin: 0 auto;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

.metric-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px; padding: 18px; text-align: center;
}
.metric-card h3 { color: #94d2bd !important; font-size: 26px; font-weight: 700; margin:0; }
.metric-card p  { color: rgba(255,255,255,0.6) !important; font-size: 11px; margin:4px 0 0; text-transform:uppercase; letter-spacing:1px; }

.result-diabetic {
    background: linear-gradient(135deg, #ffe5e7, #ffc4c7);
    border: 2px solid #e63946; border-radius: 16px;
    padding: 28px; text-align: center;
}
.result-healthy {
    background: linear-gradient(135deg, #e6f9ed, #c8f5d8);
    border: 2px solid #2dc653; border-radius: 16px;
    padding: 28px; text-align: center;
}
.result-diabetic h2 { color: #e63946 !important; }
.result-healthy  h2 { color: #1a7a38 !important; }
.result-diabetic p  { color: #7a0010 !important; }
.result-healthy  p  { color: #1a5c30 !important; }

.risk-high {
    background: rgba(230,57,70,0.1); border-left: 4px solid #e63946;
    border-radius: 8px; padding: 12px 16px; margin: 8px 0;
    color: #ff6b6b !important; font-weight: 500;
}
.risk-ok {
    background: rgba(45,198,83,0.1); border-left: 4px solid #2dc653;
    border-radius: 8px; padding: 12px 16px; margin: 8px 0;
    color: #2dc653 !important; font-weight: 500;
}

.record-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 16px; margin-bottom: 12px;
}

section[data-testid="stSidebar"] {
    background: #0d1b2a !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * { color: white !important; }

.stButton > button {
    background: linear-gradient(135deg, #0a9396, #005f73) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 12px 32px !important;
    font-family: Poppins, sans-serif !important;
    font-weight: 600 !important; font-size: 15px !important;
    width: 100% !important; transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(10,147,150,0.4) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #2dc653, #1a7a38) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 12px 32px !important;
    font-family: Poppins, sans-serif !important;
    font-weight: 600 !important; font-size: 15px !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD SAVED RECORDS FROM FILE ──────────────────────────
RECORDS_FILE = "saved_records.csv"

def load_records():
    if os.path.exists(RECORDS_FILE):
        try:
            df = pd.read_csv(RECORDS_FILE)
            return df.to_dict('records')
        except:
            return []
    return []

def save_records_to_file(records):
    if records:
        df = pd.DataFrame(records)
        df.to_csv(RECORDS_FILE, index=False)

import os

# ── SESSION STATE ──────────────────────────────────────────
if "logged_in"        not in st.session_state: st.session_state.logged_in        = False
if "page"             not in st.session_state: st.session_state.page             = "🏠 Home"
if "records"          not in st.session_state: st.session_state.records          = load_records()
if "last_prediction"  not in st.session_state: st.session_state.last_prediction  = None
if "last_inputs"      not in st.session_state: st.session_state.last_inputs      = None
if "patient_details"  not in st.session_state: st.session_state.patient_details  = {}

# ══════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    st.markdown("""
    <div style='text-align:center; padding:40px 0 16px;'>
        <div style='font-size:52px;'>🩺</div>
        <h1 style='color:white !important; font-size:30px; font-weight:700; margin:8px 0 4px;'>DiabetesAI</h1>
        <p style='color:rgba(255,255,255,0.5) !important; font-size:13px;'>Smart Diabetes Prediction & Health Management System</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white !important; text-align:center; margin-bottom:4px;'>Welcome Back 👋</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:rgba(255,255,255,0.5) !important; text-align:center; font-size:12px; margin-bottom:20px;'>Login to access the system</p>", unsafe_allow_html=True)

        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔒 Password", placeholder="Enter password", type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔐 LOGIN"):
            if username == "admin" and password == "diabetes13":
                st.session_state.logged_in = True
                st.success("✅ Login Successful!")
                st.rerun()
            elif username == "" or password == "":
                st.error("⚠️ Please enter username and password!")
            else:
                st.error("❌ Wrong username or password!")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background:rgba(10,147,150,0.1); border:1px solid rgba(10,147,150,0.3); border-radius:10px; padding:10px; text-align:center;'>
            <p style='color:rgba(255,255,255,0.7) !important; font-size:12px; margin:0;'>
            🔑 Username: <b style='color:#94d2bd;'>admin</b> &nbsp;|&nbsp;
            Password: <b style='color:#94d2bd;'>diabetes13</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════
else:

    st.markdown("""
    <div style='text-align:center; padding:12px 0 6px;'>
        <span style='font-size:28px;'>🩺</span>
        <h2 style='color:white !important; font-weight:700; margin:4px 0 2px;'>Diabetes Prediction</h2>
        <p style='color:rgba(255,255,255,0.45) !important; font-size:11px;'>Smart Diabetes Prediction </p>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("🏠", "Home"),
        ("👤", "Patient Details"),
        ("🔬", "Prediction"),
        ("⚠️", "Risk Factors"),
        ("🏥", "Health Recommendations"),
        ("📋", "Saved Records"),
    ]

    cols = st.columns(len(pages) + 1)

    for i, (icon, label) in enumerate(pages):
        with cols[i]:
            full     = f"{icon} {label}"
            selected = st.session_state.page == full
            style    = "background:rgba(10,147,150,0.3); border:1.5px solid #0a9396; box-shadow:0 4px 16px rgba(10,147,150,0.3);" if selected else "background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);"
            st.markdown(f"""
            <div style='{style} border-radius:14px; padding:12px 6px; text-align:center; margin-bottom:4px;'>
                <div style='font-size:22px;'>{icon}</div>
                <div style='font-size:9px; color:rgba(255,255,255,0.8); font-weight:500; text-transform:uppercase; letter-spacing:0.8px; margin-top:4px;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.session_state.page = full
                st.rerun()

    with cols[6]:
        st.markdown("""
        <div style='background:rgba(230,57,70,0.1); border:1px solid rgba(230,57,70,0.3); border-radius:14px; padding:12px 6px; text-align:center; margin-bottom:4px;'>
            <div style='font-size:22px;'>🚪</div>
            <div style='font-size:9px; color:rgba(230,57,70,0.9); font-weight:500; text-transform:uppercase; letter-spacing:0.8px; margin-top:4px;'>Logout</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout", use_container_width=True):
            st.session_state.logged_in       = False
            st.session_state.page            = "🏠 Home"
            st.session_state.last_prediction = None
            st.session_state.last_inputs     = None
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:6px 0 20px;'>", unsafe_allow_html=True)

    page = st.session_state.page

    # ════════════════════════════════════════════════════
    # PAGE 1: HOME
    # ════════════════════════════════════════════════════
    if page == "🏠 Home":
        st.markdown("""
        <div class='header-box'>
            <h1>🏠 Welcome to Diabetes Prediction</h1>
            <p>Instant Diabetes Prediction</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:rgba(10,147,150,0.12); border:1.5px solid rgba(10,147,150,0.4); border-radius:16px; padding:28px 32px; margin-bottom:20px;'>
            <h3 style='color:#94d2bd !important; font-size:18px; margin-bottom:14px;'>🩺 About This App</h3>
            <p style='color:rgba(255,255,255,0.85) !important; font-size:14px; line-height:2;'>
            This application is designed to
            <b style='color:#94d2bd;'>predict whether a person is Diabetic or Not Diabetic</b>
            based on their personal and medical details.
            By entering key health parameters,
            the system instantly analyzes the data and provides an accurate prediction result.
            The app also shows detailed
            <b style='color:#94d2bd;'>Risk Factor Analysis</b>
            for each medical parameter and gives
            <b style='color:#94d2bd;'>Personalized Health Recommendations</b>
            including diet, exercise, medical advice and lifestyle changes.
            All patient records are
            <b style='color:#94d2bd;'>Permanently Saved</b>
            and can be downloaded as documents for future medical reference.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class='card' style='text-align:center;'>
                <div style='font-size:36px; margin-bottom:12px;'>👤</div>
                <h4>Patient Details</h4>
                <p style='font-size:13px; color:rgba(255,255,255,0.8) !important;'>Enter patient personal information like name, age, gender, blood group and contact details.</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='card' style='text-align:center;'>
                <div style='font-size:36px; margin-bottom:12px;'>🔬</div>
                <h4>Diabetes Prediction</h4>
                <p style='font-size:13px; color:rgba(255,255,255,0.8) !important;'>Enter medical parameters and get instant prediction — Diabetic or Not Diabetic with probability percentage.</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class='card' style='text-align:center;'>
                <div style='font-size:36px; margin-bottom:12px;'>📋</div>
                <h4>Save & Download</h4>
                <p style='font-size:13px; color:rgba(255,255,255,0.8) !important;'>All patient records are permanently saved and can be downloaded as CSV or health report document.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class='card'>
            <h4>🚀 How to Use This App?</h4>
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:8px;'>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;'>1</span>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Click <b style='color:#94d2bd;'>👤 Patient Details</b> — enter personal info</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;'>2</span>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Click <b style='color:#94d2bd;'>🔬 Prediction</b> — enter medical details</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;'>3</span>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Click <b style='color:#94d2bd;'>⚡ Predict Now</b> — get result instantly</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;'>4</span>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Check <b style='color:#94d2bd;'>⚠️ Risk Factors</b> for analysis</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;'>5</span>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Get tips from <b style='color:#94d2bd;'>🏥 Health Recommend</b></p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:26px; height:26px; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; flex-shrink:0;'>6</span>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Download report from <b style='color:#94d2bd;'>📋 Saved Records</b></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # PAGE 2: PATIENT DETAILS
    # ════════════════════════════════════════════════════
    elif page == "👤 Patient Details":
        st.markdown("""
        <div class='header-box'>
            <h1>👤 Patient Personal Details</h1>
            <p>Enter patient information before prediction</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'><h4>👤 Personal Information</h4>", unsafe_allow_html=True)
            name   = st.text_input("Full Name",    placeholder="Enter patient full name")
            age    = st.number_input("Age",         min_value=1, max_value=120, value=30)
            gender = st.selectbox("Gender",         ["Male", "Female", "Other"])
            dob    = st.text_input("Date of Birth", placeholder="DD/MM/YYYY")
            blood  = st.selectbox("Blood Group",    ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'><h4>📞 Contact Information</h4>", unsafe_allow_html=True)
            phone   = st.text_input("Phone Number",  placeholder="Enter phone number")
            email   = st.text_input("Email Address", placeholder="Enter email address")
            address = st.text_area("Address",        placeholder="Enter full address", height=80)
            city    = st.text_input("City",          placeholder="Enter city")
            state   = st.text_input("State",         placeholder="Enter state")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h4>🏥 Medical History</h4>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            family_history = st.selectbox("Family History of Diabetes",  ["No", "Yes — Father", "Yes — Mother", "Yes — Both Parents", "Yes — Siblings"])
            existing       = st.selectbox("Existing Medical Conditions",  ["None", "Hypertension", "Obesity", "Heart Disease", "Kidney Disease", "Other"])
        with col4:
            medications = st.text_input("Current Medications", placeholder="Enter current medications if any")
            allergies   = st.text_input("Known Allergies",     placeholder="Enter allergies if any")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("💾 SAVE PATIENT DETAILS"):
            if name == "":
                st.error("⚠️ Please enter patient name!")
            else:
                st.session_state.patient_details = {
                    "name": name, "age": age, "gender": gender,
                    "dob": dob, "blood_group": blood,
                    "phone": phone, "email": email,
                    "address": address, "city": city, "state": state,
                    "family_history": family_history,
                    "existing_conditions": existing,
                    "medications": medications,
                    "allergies": allergies,
                    "date": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                st.success(f"✅ Patient details saved for {name}!")
                st.info("👉 Now go to 🔬 Prediction page!")

        if st.session_state.patient_details:
            p = st.session_state.patient_details
            st.markdown(f"""
            <div style='background:rgba(10,147,150,0.1); border:1px solid rgba(10,147,150,0.3); border-radius:12px; padding:14px 16px; margin-top:16px;'>
                <p style='color:#94d2bd !important; font-weight:600; margin-bottom:6px;'>✅ Current Patient Saved:</p>
                <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>
                👤 <b>{p.get('name','')}</b> &nbsp;|&nbsp;
                🎂 Age: {p.get('age','')} &nbsp;|&nbsp;
                ⚧ {p.get('gender','')} &nbsp;|&nbsp;
                🩸 {p.get('blood_group','')} &nbsp;|&nbsp;
                📅 {p.get('date','')}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # PAGE 3: PREDICTION
    # ════════════════════════════════════════════════════
    elif page == "🔬 Prediction":
        st.markdown("""
        <div class='header-box'>
            <h1>🔬 Diabetes Prediction</h1>
            <p>Enter patient medical details for prediction</p>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.patient_details:
            p = st.session_state.patient_details
            st.markdown(f"""
            <div style='background:rgba(10,147,150,0.1); border:1px solid rgba(10,147,150,0.3); border-radius:10px; padding:12px 16px; margin-bottom:16px;'>
                <p style='color:#94d2bd !important; margin:0; font-size:13px;'>
                👤 Patient: <b style='color:white;'>{p.get('name','')}</b> &nbsp;|&nbsp;
                Age: <b style='color:white;'>{p.get('age','')}</b> &nbsp;|&nbsp;
                Gender: <b style='color:white;'>{p.get('gender','')}</b> &nbsp;|&nbsp;
                Blood Group: <b style='color:white;'>{p.get('blood_group','')}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please fill Patient Details first! Go to 👤 Patient Details page.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'><h4>🩸 Blood Parameters</h4>", unsafe_allow_html=True)
            glucose = st.number_input("Glucose Level (mg/dL)",  min_value=0,   max_value=300,  value=100, step=1,    help="Normal: 70–140 mg/dL")
            insulin = st.number_input("Insulin Level (μU/mL)",  min_value=0,   max_value=900,  value=80,  step=1,    help="Normal: 16–166 μU/mL")
            bp      = st.number_input("Blood Pressure (mmHg)",  min_value=0,   max_value=200,  value=70,  step=1,    help="Normal: 60–90 mmHg")
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'><h4>📊 Body Parameters</h4>", unsafe_allow_html=True)
            bmi     = st.number_input("BMI (kg/m²)",                min_value=0.0, max_value=70.0, value=25.0, step=0.1,   help="Normal: 18.5–24.9")
            dpf     = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0,  value=0.5,  step=0.001, format="%.3f", help="Range: 0.08–2.42")
            age_val = st.number_input("Age (years)",                min_value=1,   max_value=120,  value=30,   step=1,     help="Range: 21–81")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("⚡ PREDICT NOW"):
            features        = np.array([[glucose, bp, insulin, bmi, dpf, age_val]])
            features_scaled = scaler.transform(features)
            prediction      = int(model.predict(features_scaled)[0])
            probability     = float(model.predict_proba(features_scaled)[0][1]) * 100

            st.session_state.last_prediction  = prediction
            st.session_state.last_probability = probability
            st.session_state.last_inputs = {
                "glucose": glucose, "bp": bp,
                "insulin": insulin, "bmi": bmi,
                "dpf": dpf, "age": age_val
            }

            # ✅ Auto save record permanently
            record = {
                "date":               datetime.now().strftime("%d/%m/%Y %H:%M"),
                "patient":            st.session_state.patient_details.get("name",               "Unknown"),
                "age":                st.session_state.patient_details.get("age",                age_val),
                "gender":             st.session_state.patient_details.get("gender",             "—"),
                "blood_group":        st.session_state.patient_details.get("blood_group",        "—"),
                "phone":              st.session_state.patient_details.get("phone",              "—"),
                "email":              st.session_state.patient_details.get("email",              "—"),
                "address":            st.session_state.patient_details.get("address",            "—"),
                "city":               st.session_state.patient_details.get("city",               "—"),
                "state":              st.session_state.patient_details.get("state",              "—"),
                "family_history":     st.session_state.patient_details.get("family_history",     "—"),
                "existing_conditions":st.session_state.patient_details.get("existing_conditions","—"),
                "medications":        st.session_state.patient_details.get("medications",        "—"),
                "allergies":          st.session_state.patient_details.get("allergies",          "—"),
                "glucose":            glucose,
                "bp":                 bp,
                "insulin":            insulin,
                "bmi":                bmi,
                "dpf":                dpf,
                "age_val":            age_val,
                "result":             "DIABETIC" if prediction == 1 else "NOT DIABETIC",
                "probability":        round(probability, 1)
            }
            st.session_state.records.append(record)
            save_records_to_file(st.session_state.records)

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                if prediction == 1:
                    st.markdown(f"""
                    <div class='result-diabetic'>
                        <div style='font-size:48px;'>⚠️</div>
                        <h2>DIABETIC</h2>
                        <p style='font-size:14px; margin:8px 0;'>High diabetes risk detected</p>
                        <p style='font-size:13px;'>Probability: <b>{probability:.1f}%</b></p>
                        <div style='background:rgba(0,0,0,0.1); border-radius:100px; height:10px; margin:10px 0; overflow:hidden;'>
                            <div style='width:{probability}%; height:100%; background:linear-gradient(90deg,#e63946,#ff8fa3); border-radius:100px;'></div>
                        </div>
                        <p style='font-size:12px;'>⚠️ Please consult a doctor immediately</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    hp = 100 - probability
                    st.markdown(f"""
                    <div class='result-healthy'>
                        <div style='font-size:48px;'>✅</div>
                        <h2>NOT DIABETIC</h2>
                        <p style='font-size:14px; margin:8px 0;'>Low diabetes risk detected</p>
                        <p style='font-size:13px;'>Healthy Probability: <b>{hp:.1f}%</b></p>
                        <div style='background:rgba(0,0,0,0.1); border-radius:100px; height:10px; margin:10px 0; overflow:hidden;'>
                            <div style='width:{hp}%; height:100%; background:linear-gradient(90deg,#2dc653,#69f0ae); border-radius:100px;'></div>
                        </div>
                        <p style='font-size:12px;'>✅ Maintain your healthy lifestyle!</p>
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='card'><h4>⚡ Quick Risk Check</h4>", unsafe_allow_html=True)
                risks = [
                    ("🩸 Glucose",        glucose,  70,   140,  "mg/dL"),
                    ("⚖️ BMI",            bmi,      18.5, 24.9, "kg/m²"),
                    ("🎂 Age",            age_val,  0,    45,   "yrs"),
                    ("💉 Insulin",        insulin,  16,   166,  "μU/mL"),
                    ("🫀 Blood Pressure", bp,       60,   90,   "mmHg"),
                ]
                for name_r, val, low, high, unit in risks:
                    if val < low or val > high:
                        st.markdown(f"<div class='risk-high'>⚠️ {name_r}: {val} {unit} — Abnormal</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='risk-ok'>✅ {name_r}: {val} {unit} — Normal</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.success("✅ Record permanently saved! Go to 📋 Saved Records to download.")

    # ════════════════════════════════════════════════════
    # PAGE 4: RISK FACTORS
    # ════════════════════════════════════════════════════
    elif page == "⚠️ Risk Factors":
        st.markdown("""
        <div class='header-box'>
            <h1>⚠️ Risk Factor Analysis</h1>
            <p>Detailed analysis of each medical parameter</p>
        </div>
        """, unsafe_allow_html=True)

        inputs = st.session_state.last_inputs
        if inputs is None:
            st.warning("⚠️ Please run a prediction first from the 🔬 Prediction page!")
        else:
            risk_factors = [
                ("🩸 Glucose",           inputs["glucose"], 70,   140,  "mg/dL", "Primary diabetes indicator. High glucose means cells are not absorbing sugar properly. Values above 140 indicate diabetes."),
                ("⚖️ BMI",               inputs["bmi"],     18.5, 24.9, "kg/m²", "Body Mass Index. Higher BMI means obesity which directly causes insulin resistance leading to Type 2 diabetes."),
                ("🎂 Age",               inputs["age"],     0,    45,   "years",  "Risk increases with age. People above 45 are at significantly higher risk of developing Type 2 diabetes."),
                ("💉 Insulin",           inputs["insulin"], 16,   166,  "μU/mL", "Insulin regulates blood sugar. Abnormal levels indicate pancreatic dysfunction and poor glucose metabolism."),
                ("🫀 Blood Pressure",    inputs["bp"],      60,   90,   "mmHg",  "High blood pressure is strongly associated with diabetes and increases risk of heart and kidney problems."),
                ("🧬 Diabetes Pedigree", inputs["dpf"],     0,    0.8,  "score",  "Genetic risk factor. Higher score means stronger family history of diabetes. Hereditary factor plays a key role."),
            ]

            col1, col2 = st.columns(2)
            for i, (name_r, val, low, high, unit, desc) in enumerate(risk_factors):
                col = col1 if i % 2 == 0 else col2
                with col:
                    is_risk = val < low or val > high
                    color  = "#ff6b6b" if is_risk else "#2dc653"
                    bg     = "rgba(230,57,70,0.08)" if is_risk else "rgba(45,198,83,0.08)"
                    border = "#e63946" if is_risk else "#2dc653"
                    status = "🔴 HIGH RISK" if is_risk else "🟢 NORMAL"
                    st.markdown(f"""
                    <div style='background:{bg}; border:1px solid {border}; border-radius:12px; padding:18px; margin-bottom:14px;'>
                        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                            <b style='color:white; font-size:14px;'>{name_r}</b>
                            <span style='color:{color}; font-size:11px; font-weight:600;'>{status}</span>
                        </div>
                        <div style='font-size:20px; font-weight:700; color:{color}; margin-bottom:4px;'>{val} <span style='font-size:12px; font-weight:400; color:rgba(255,255,255,0.5);'>{unit}</span></div>
                        <div style='font-size:10px; color:rgba(255,255,255,0.55); margin-bottom:8px;'>Normal: {low} – {high} {unit}</div>
                        <div style='font-size:12px; color:rgba(255,255,255,0.75); line-height:1.6;'>{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # PAGE 5: HEALTH RECOMMENDATION
    # ════════════════════════════════════════════════════
    elif page == "🏥 Health Recommendations":
        st.markdown("""
        <div class='header-box'>
            <h1>🏥 Health Recommendation</h1>
            <p>Personalized health recommendations based on your result</p>
        </div>
        """, unsafe_allow_html=True)

        prediction = st.session_state.last_prediction
        if prediction is None:
            st.warning("⚠️ Please run a prediction first from the 🔬 Prediction page!")
        else:
            if prediction == 1:
                st.markdown("""
                <div style='background:rgba(230,57,70,0.1); border:1px solid #e63946; border-radius:14px; padding:18px; margin-bottom:20px;'>
                    <h3 style='color:#e63946 !important; margin-bottom:4px;'>⚠️ High Risk — Please Follow These Recommendations</h3>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Your result indicates high diabetes risk. Strictly follow the below health guidelines.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background:rgba(45,198,83,0.1); border:1px solid #2dc653; border-radius:14px; padding:18px; margin-bottom:20px;'>
                    <h3 style='color:#2dc653 !important; margin-bottom:4px;'>✅ Low Risk — Maintain Your Healthy Lifestyle</h3>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0; font-size:13px;'>Your result shows low diabetes risk. Follow these tips to stay healthy.</p>
                </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div class='card'>
                    <h4>🥗 Diet Recommendations</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2.2; padding-left:18px; font-size:13px;'>
                        <li>Avoid sugary drinks, sweets and desserts</li>
                        <li>Eat more green vegetables and fresh fruits</li>
                        <li>Choose whole grains — brown rice, wheat bread</li>
                        <li>Limit white rice, white bread and fried foods</li>
                        <li>Drink 8 to 10 glasses of water daily</li>
                        <li>Eat small meals every 3 to 4 hours</li>
                        <li>Avoid processed and packaged foods</li>
                        <li>Include more fiber rich foods in diet</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class='card'>
                    <h4>🏃 Exercise Recommendations</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2.2; padding-left:18px; font-size:13px;'>
                        <li>Walk briskly for at least 30 minutes daily</li>
                        <li>Do light exercises 5 days a week</li>
                        <li>Try yoga, swimming or cycling</li>
                        <li>Avoid sitting for more than 1 hour</li>
                        <li>Maintain healthy body weight</li>
                        <li>Do stretching exercises every morning</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class='card'>
                    <h4>🏥 Medical Advice</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2.2; padding-left:18px; font-size:13px;'>
                        <li>Consult a doctor immediately if high risk</li>
                        <li>Check blood sugar levels every 3 months</li>
                        <li>Monitor blood pressure every week</li>
                        <li>Get HbA1c test done every 3 months</li>
                        <li>Take prescribed medicines regularly</li>
                        <li>Never skip doctor appointments</li>
                        <li>Get eye and kidney checkup annually</li>
                        <li>Monitor cholesterol levels regularly</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class='card'>
                    <h4>😴 Lifestyle Changes</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2.2; padding-left:18px; font-size:13px;'>
                        <li>Sleep 7 to 8 hours every night</li>
                        <li>Completely avoid smoking and alcohol</li>
                        <li>Practice meditation to manage stress</li>
                        <li>Track daily food and water intake</li>
                        <li>Stay positive and mentally healthy</li>
                        <li>Reduce screen time before sleep</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # PAGE 6: SAVED RECORDS
    # ════════════════════════════════════════════════════
    elif page == "📋 Saved Records":
        st.markdown("""
        <div class='header-box'>
            <h1>📋 Saved Patient Records</h1>
            <p>All records are permanently saved — view and download anytime</p>
        </div>
        """, unsafe_allow_html=True)

        # Reload from file every time
        st.session_state.records = load_records()

        if not st.session_state.records:
            st.info("📭 No records saved yet. Run a prediction to save records!")
        else:
            total    = len(st.session_state.records)
            diabetic = sum(1 for r in st.session_state.records if r['result'] == 'DIABETIC')
            healthy  = total - diabetic

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='metric-card'><h3>{total}</h3><p>Total Records</p></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div class='metric-card'><h3 style='color:#ff6b6b !important;'>{diabetic}</h3><p>Diabetic</p></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='metric-card'><h3 style='color:#2dc653 !important;'>{healthy}</h3><p>Not Diabetic</p></div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            for i, r in enumerate(reversed(st.session_state.records)):
                color = "#ff6b6b" if r['result'] == 'DIABETIC' else "#2dc653"
                icon  = "⚠️" if r['result'] == 'DIABETIC' else "✅"
                st.markdown(f"""
                <div class='record-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;'>
                        <div>
                            <span style='color:white; font-size:15px; font-weight:600;'>{icon} {r['patient']}</span>
                            <span style='color:rgba(255,255,255,0.45); font-size:11px; margin-left:12px;'>📅 {r['date']}</span>
                        </div>
                        <span style='color:{color}; font-weight:700; font-size:13px; background:rgba(255,255,255,0.05); padding:4px 12px; border-radius:100px; border:1px solid {color};'>{r['result']} — {r['probability']}%</span>
                    </div>
                    <div style='display:grid; grid-template-columns:repeat(6,1fr); gap:8px;'>
                        <div style='background:rgba(255,255,255,0.04); border-radius:8px; padding:8px; text-align:center;'>
                            <div style='font-size:10px; color:rgba(255,255,255,0.45);'>Age</div>
                            <div style='font-size:13px; color:white; font-weight:600;'>{r['age']}</div>
                        </div>
                        <div style='background:rgba(255,255,255,0.04); border-radius:8px; padding:8px; text-align:center;'>
                            <div style='font-size:10px; color:rgba(255,255,255,0.45);'>Gender</div>
                            <div style='font-size:13px; color:white; font-weight:600;'>{r['gender']}</div>
                        </div>
                        <div style='background:rgba(255,255,255,0.04); border-radius:8px; padding:8px; text-align:center;'>
                            <div style='font-size:10px; color:rgba(255,255,255,0.45);'>Glucose</div>
                            <div style='font-size:13px; color:white; font-weight:600;'>{r['glucose']}</div>
                        </div>
                        <div style='background:rgba(255,255,255,0.04); border-radius:8px; padding:8px; text-align:center;'>
                            <div style='font-size:10px; color:rgba(255,255,255,0.45);'>BMI</div>
                            <div style='font-size:13px; color:white; font-weight:600;'>{r['bmi']}</div>
                        </div>
                        <div style='background:rgba(255,255,255,0.04); border-radius:8px; padding:8px; text-align:center;'>
                            <div style='font-size:10px; color:rgba(255,255,255,0.45);'>BP</div>
                            <div style='font-size:13px; color:white; font-weight:600;'>{r['bp']}</div>
                        </div>
                        <div style='background:rgba(255,255,255,0.04); border-radius:8px; padding:8px; text-align:center;'>
                            <div style='font-size:10px; color:rgba(255,255,255,0.45);'>Insulin</div>
                            <div style='font-size:13px; color:white; font-weight:600;'>{r['insulin']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── DOWNLOAD CSV ─────────────────────────────
            df_records = pd.DataFrame(st.session_state.records)
            csv_data   = df_records.to_csv(index=False)

            st.download_button(
                label="📥 DOWNLOAD ALL RECORDS (CSV)",
                data=csv_data,
                file_name=f"patient_records_{datetime.now().strftime('%d%m%Y_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── DOWNLOAD TEXT REPORT ─────────────────────
            report_lines = []
            report_lines.append("=" * 60)
            report_lines.append("       DIABETES PREDICTION — PATIENT HEALTH REPORT")
            report_lines.append("=" * 60)
            report_lines.append(f"Generated on  : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            report_lines.append(f"Total Records : {total}")
            report_lines.append(f"Diabetic      : {diabetic}")
            report_lines.append(f"Not Diabetic  : {healthy}")
            report_lines.append("=" * 60)

            for i, r in enumerate(st.session_state.records, 1):
                report_lines.append(f"\nRecord #{i}")
                report_lines.append("-" * 40)
                report_lines.append(f"Patient Name       : {r['patient']}")
                report_lines.append(f"Date               : {r['date']}")
                report_lines.append(f"Age                : {r['age']}")
                report_lines.append(f"Gender             : {r['gender']}")
                report_lines.append(f"Blood Group        : {r['blood_group']}")
                report_lines.append(f"Phone              : {r['phone']}")
                report_lines.append(f"Email              : {r['email']}")
                report_lines.append(f"Address            : {r['address']}, {r['city']}, {r['state']}")
                report_lines.append(f"Family History     : {r['family_history']}")
                report_lines.append(f"Existing Conditions: {r['existing_conditions']}")
                report_lines.append(f"Medications        : {r['medications']}")
                report_lines.append(f"Allergies          : {r['allergies']}")
                report_lines.append(f"Glucose            : {r['glucose']} mg/dL")
                report_lines.append(f"Blood Pressure     : {r['bp']} mmHg")
                report_lines.append(f"Insulin            : {r['insulin']} μU/mL")
                report_lines.append(f"BMI                : {r['bmi']} kg/m²")
                report_lines.append(f"DPF Score          : {r['dpf']}")
                report_lines.append(f"Prediction Result  : {r['result']}")
                report_lines.append(f"Probability        : {r['probability']}%")
                report_lines.append("-" * 40)

            report_lines.append("\n" + "=" * 60)
            report_lines.append("Diabetes Prediction — Smart Diabetes Prediction")
            report_lines.append("For educational purposes only. Not a substitute for medical advice.")
            report_lines.append("=" * 60)

            report_text = "\n".join(report_lines)

            st.download_button(
                label="📄 DOWNLOAD HEALTH REPORT (TXT)",
                data=report_text,
                file_name=f"health_report_{datetime.now().strftime('%d%m%Y_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🗑️ CLEAR ALL RECORDS"):
                st.session_state.records = []
                if os.path.exists(RECORDS_FILE):
                    os.remove(RECORDS_FILE)
                st.success("✅ All records cleared!")
                st.rerun()
