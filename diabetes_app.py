import streamlit as st
import sqlite3
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
from fpdf import FPDF
import time
import hashlib
import plotly.express as px
import plotly.graph_objects as go

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════
# CSS — LUXURY MEDICAL DARK THEME
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

:root {
  --bg:       #060d18;
  --bg2:      #0b1628;
  --card:     #0f1f35;
  --card2:    #142540;
  --teal:     #0fd4c8;
  --teal2:    #06a89e;
  --gold:     #f0b429;
  --red:      #ff4560;
  --green:    #00e396;
  --text:     #e8f0f8;
  --muted:    #5a7a9a;
  --border:   rgba(15,212,200,0.12);
}

* { margin:0; padding:0; box-sizing:border-box; }

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(15,212,200,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(240,180,41,0.03) 0%, transparent 50%) !important;
}

/* ── HIDE STREAMLIT ELEMENTS ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display:none; }
[data-testid="stToolbar"] { display:none; }

/* ── INPUTS ── */
.stTextInput input,
.stNumberInput input {
    background: var(--card2) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
}
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(15,212,200,0.12) !important;
}
.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: var(--muted) !important;
}

/* ── SELECT BOX ── */
.stSelectbox div[data-baseweb="select"] {
    background: var(--card2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
}
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] div {
    color: var(--text) !important;
    background: var(--card2) !important;
    font-family: 'Outfit', sans-serif !important;
}
.stSelectbox svg { fill: var(--teal) !important; }
[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
[data-baseweb="popover"] li,
[data-baseweb="menu"] li {
    color: var(--text) !important;
    background: var(--card) !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-baseweb="popover"] li:hover,
[data-baseweb="menu"] li:hover {
    background: var(--card2) !important;
    color: var(--teal) !important;
}

/* ── LABELS ── */
label {
    color: var(--muted) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--teal2)) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(15,212,200,0.35) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #e63946, #9b1d24) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    width: 100% !important;
}

/* ── DATAFRAME ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--teal2); border-radius: 3px; }

/* ── CUSTOM COMPONENTS ── */
.hero-header {
    background: linear-gradient(135deg, var(--card) 0%, var(--card2) 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    text-align: center;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at center, rgba(15,212,200,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px;
    font-weight: 800;
    color: white !important;
    margin: 0 0 6px;
}
.hero-sub {
    color: var(--muted) !important;
    font-size: 13px;
}

.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, border-color 0.2s;
}
.stat-card:hover {
    transform: translateY(-3px);
    border-color: rgba(15,212,200,0.3);
}
.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--teal), transparent);
}
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 32px;
    font-weight: 800;
    color: var(--teal);
    line-height: 1;
}
.stat-lbl {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
}

.glass-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
}
.glass-card h4 {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--teal) !important;
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 8px;
}

.login-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 44px 40px;
    max-width: 460px;
    margin: 0 auto;
    box-shadow: 0 30px 80px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}
.login-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--teal), var(--gold));
}

.result-box {
    border-radius: 18px;
    padding: 32px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-box.danger {
    background: linear-gradient(135deg, rgba(255,69,96,0.12), rgba(155,29,36,0.08));
    border: 1.5px solid rgba(255,69,96,0.35);
}
.result-box.safe {
    background: linear-gradient(135deg, rgba(0,227,150,0.1), rgba(0,150,100,0.06));
    border: 1.5px solid rgba(0,227,150,0.3);
}
.result-emoji { font-size: 52px; display: block; margin-bottom: 12px; }
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 8px;
}
.danger .result-title { color: var(--red) !important; }
.safe   .result-title { color: var(--green) !important; }

.risk-tag-high {
    background: rgba(255,69,96,0.1);
    border-left: 3px solid var(--red);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    color: #ff7890 !important;
    font-size: 13px;
    font-weight: 500;
}
.risk-tag-ok {
    background: rgba(0,227,150,0.08);
    border-left: 3px solid var(--green);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 6px 0;
    color: #00e396 !important;
    font-size: 13px;
    font-weight: 500;
}

.rec-box {
    background: linear-gradient(135deg, rgba(15,212,200,0.08), rgba(6,168,158,0.05));
    border: 1px solid rgba(15,212,200,0.2);
    border-radius: 14px;
    padding: 20px 24px;
    margin-top: 16px;
}
.rec-box h4 { color: var(--teal) !important; font-size: 15px; margin-bottom: 10px; }

.record-row {
    background: var(--card2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.2s;
}
.record-row:hover { border-color: rgba(15,212,200,0.3); }

.nav-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.2s;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--muted);
    text-transform: uppercase;
}
.nav-pill.active {
    background: rgba(15,212,200,0.15);
    border-color: var(--teal);
    color: var(--teal);
}

.patient-badge {
    background: rgba(15,212,200,0.08);
    border: 1px solid rgba(15,212,200,0.2);
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 16px;
    font-size: 13px;
    color: var(--text) !important;
}

.prob-bar-bg {
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    height: 8px;
    overflow: hidden;
    margin: 10px 0;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 1s ease;
}

/* TOAST / BADGE */
.badge-diabetic {
    display: inline-block;
    background: rgba(255,69,96,0.15);
    color: var(--red);
    border: 1px solid rgba(255,69,96,0.3);
    border-radius: 100px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-healthy {
    display: inline-block;
    background: rgba(0,227,150,0.12);
    color: var(--green);
    border: 1px solid rgba(0,227,150,0.25);
    border-radius: 100px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* PULSE DOT */
.pulse-dot {
    width: 8px; height: 8px;
    background: var(--green);
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.4; transform:scale(0.8); }
}

/* SECTION DIVIDER */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 24px 0;
}

p { color: var(--text) !important; }
li { color: rgba(232,240,248,0.8) !important; }
h1,h2,h3,h4,h5,h6 { color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════
conn = sqlite3.connect("diabetespro.db", check_same_thread=False)
c    = conn.cursor()

def create_tables():
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT UNIQUE NOT NULL,
            password  TEXT NOT NULL,
            fullname  TEXT DEFAULT '',
            email     TEXT DEFAULT '',
            role      TEXT DEFAULT 'user',
            joined    TEXT
        )
    """)
    for col in ["fullname TEXT DEFAULT ''", "email TEXT DEFAULT ''",
                "role TEXT DEFAULT 'user'", "joined TEXT DEFAULT ''"]:
        try: c.execute(f"ALTER TABLE users ADD COLUMN {col}"); conn.commit()
        except: pass

    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE,
            username   TEXT,
            name       TEXT,
            age        INTEGER,
            sex        TEXT,
            phone      TEXT DEFAULT '',
            blood_grp  TEXT DEFAULT '',
            created    TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            username       TEXT,
            patient_id     TEXT,
            patient_name   TEXT,
            age            INTEGER,
            sex            TEXT,
            glucose        REAL,
            bp             REAL,
            insulin        REAL,
            bmi            REAL,
            dpf            REAL,
            result         TEXT,
            probability    REAL,
            risk_level     TEXT,
            recommendation TEXT,
            date           TEXT
        )
    """)
    for col in ["patient_id TEXT DEFAULT ''", "risk_level TEXT DEFAULT ''",
                "dpf REAL DEFAULT 0"]:
        try: c.execute(f"ALTER TABLE records ADD COLUMN {col}"); conn.commit()
        except: pass

    # Admin user
    try:
        pw = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute("INSERT OR IGNORE INTO users (username,password,fullname,email,role,joined) VALUES (?,?,?,?,?,?)",
                  ("admin", pw, "Administrator", "admin@diabetespro.com", "admin",
                   datetime.now().strftime("%d/%m/%Y")))
        conn.commit()
    except: pass

create_tables()

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def add_user(username, password, fullname, email):
    try:
        c.execute("INSERT INTO users (username,password,fullname,email,role,joined) VALUES (?,?,?,?,?,?)",
                  (username, hash_pw(password), fullname, email, "user",
                   datetime.now().strftime("%d/%m/%Y")))
        conn.commit(); return True
    except: return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_pw(password)))
    row = c.fetchone()
    if row: return {"id":row[0],"username":row[1],"fullname":row[3],"email":row[4],"role":row[5]}
    return None

def generate_patient_id():
    c.execute("SELECT COUNT(*) FROM patients")
    n = c.fetchone()[0]
    return f"PT{str(n+1).zfill(4)}"

def save_patient(username, name, age, sex, phone, blood_grp):
    pid = generate_patient_id()
    try:
        c.execute("INSERT INTO patients (patient_id,username,name,age,sex,phone,blood_grp,created) VALUES (?,?,?,?,?,?,?,?)",
                  (pid, username, name, age, sex, phone, blood_grp,
                   datetime.now().strftime("%d/%m/%Y %H:%M")))
        conn.commit(); return pid
    except: return None

def get_patients(username):
    c.execute("SELECT * FROM patients WHERE username=? ORDER BY id DESC", (username,))
    return c.fetchall()

def add_record(data):
    c.execute("""INSERT INTO records
        (username,patient_id,patient_name,age,sex,glucose,bp,insulin,bmi,dpf,
         result,probability,risk_level,recommendation,date)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data)
    conn.commit()

def get_user_records(username):
    c.execute("SELECT * FROM records WHERE username=? ORDER BY id DESC", (username,))
    return c.fetchall()

def get_all_records():
    c.execute("SELECT * FROM records ORDER BY id DESC")
    return c.fetchall()

def get_patient_records(username, patient_id):
    c.execute("SELECT * FROM records WHERE username=? AND patient_id=? ORDER BY id DESC",
              (username, patient_id))
    return c.fetchall()

def get_all_users():
    c.execute("SELECT id,username,fullname,email,role,joined FROM users")
    return c.fetchall()

# ══════════════════════════════════════════════════════════
# MODEL
# ══════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    model  = pickle.load(open("diabetes_svm_model.pkl","rb"))
    scaler = pickle.load(open("scaler.pkl","rb"))
    return model, scaler

model, scaler = load_model()

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
for k,v in [("logged_in",False),("user",None),("page","Dashboard"),
            ("auth_tab","login"),("last_result",None),("sel_patient",None)]:
    if k not in st.session_state: st.session_state[k] = v

# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
RECORD_COLS = ["ID","Username","PatientID","Name","Age","Sex",
               "Glucose","BP","Insulin","BMI","DPF",
               "Result","Probability","RiskLevel","Recommendation","Date"]

def get_risk_level(prob):
    if prob >= 70: return "HIGH"
    if prob >= 40: return "MODERATE"
    return "LOW"

def get_recommendation(prob):
    if prob >= 70:
        return "HIGH RISK: Consult a doctor immediately. Follow strict diet, avoid sugar, exercise daily, monitor blood sugar regularly."
    if prob >= 40:
        return "MODERATE RISK: Control your diet, exercise regularly, reduce processed foods, monitor blood sugar monthly."
    return "LOW RISK: Maintain healthy lifestyle, eat balanced diet, stay active, and get regular checkups."

# ══════════════════════════════════════════════════════════
# PDF GENERATOR
def generate_pdf(title, subtitle, df):
    from fpdf import FPDF
    import os
    from datetime import datetime

    pdf = FPDF()
    pdf.add_page()

    font_path = os.path.join(os.getcwd(), "DejaVuSans.ttf")

    pdf.add_font("DejaVu", "", font_path, uni=True)
    pdf.add_font("DejaVu", "B", font_path, uni=True)

    # Header
    pdf.set_font("DejaVu", "B", 16)
    pdf.cell(0, 10, title, ln=True)

    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 8, subtitle, ln=True)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)

    pdf.ln(5)

 # Records
for i, (_, row) in enumerate(df.iterrows(), 1):
    result = str(row.get("Result", ""))
    prob = row.get("Probability", 0)
    risk = str(row.get("RiskLevel", ""))

    pdf.set_font("DejaVu", "B", 11)
    pdf.cell(0, 8, f"Record #{i} - {result} | Probability: {prob}% | Risk: {risk}", ln=True)

    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 6, f"Date: {row.get('Date','-')}", ln=True)
    pdf.cell(0, 6, f"Age: {row.get('Age','-')}", ln=True)
    pdf.cell(0, 6, f"Sex: {row.get('Sex','-')}", ln=True)
    pdf.cell(0, 6, f"Glucose: {row.get('Glucose','-')}", ln=True)
    pdf.cell(0, 6, f"BMI: {row.get('BMI','-')}", ln=True)

    rec = str(row.get("Recommendation", "-"))
    pdf.multi_cell(0, 6, f"Recommendation: {rec}")

    pdf.ln(3)

pdf_output = pdf.output(dest='S')
return pdf_output if isinstance(pdf_output, bytes) else pdf_output.encode('latin1')
# ══════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════
def show_auth():
    st.markdown("""
    <div style='text-align:center; padding:48px 0 24px;'>
        <div style='font-size:56px; margin-bottom:12px;'>🩺</div>
        <div style='font-family:"Playfair Display",serif; font-size:38px; font-weight:800; color:white; margin-bottom:8px;'>
            DiabetesAI <span style='color:#0fd4c8;'>Pro</span>
        </div>
        <p style='color:#5a7a9a; font-size:14px; letter-spacing:2px; text-transform:uppercase;'>
            Smart Diabetes Prediction & Health Management
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        tab1, tab2 = st.columns(2)
        with tab1:
            if st.button("🔐  Login",    key="t_login"):
                st.session_state.auth_tab = "login"; st.rerun()
        with tab2:
            if st.button("📝  Register", key="t_reg"):
                st.session_state.auth_tab = "register"; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.auth_tab == "login":
            st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
            st.markdown("""
            <div style='text-align:center; margin-bottom:28px;'>
                <div style='font-family:"Playfair Display",serif; font-size:22px; font-weight:700; color:white;'>Welcome Back</div>
                <p style='color:#5a7a9a; font-size:12px; margin-top:4px;'>Sign in to your account</p>
            </div>
            """, unsafe_allow_html=True)

            u = st.text_input("Username", placeholder="Enter username", key="li_u")
            p = st.text_input("Password", placeholder="Enter password", type="password", key="li_p")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign In →"):
                if not u or not p:
                    st.error("Please fill all fields")
                else:
                    user = login_user(u, p)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user      = user
                        st.session_state.page      = "Dashboard"
                        msg = st.empty()
                        msg.success(f"✅ Welcome back, {user['fullname']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")

            st.markdown("""
            <div style='margin-top:20px; background:rgba(15,212,200,0.06); border:1px solid rgba(15,212,200,0.15); border-radius:10px; padding:10px; text-align:center;'>
                <span style='color:#5a7a9a; font-size:11px;'>Demo: </span>
                <b style='color:#0fd4c8; font-size:11px;'>admin / admin123</b>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
            st.markdown("""
            <div style='text-align:center; margin-bottom:28px;'>
                <div style='font-family:"Playfair Display",serif; font-size:22px; font-weight:700; color:white;'>Create Account</div>
                <p style='color:#5a7a9a; font-size:12px; margin-top:4px;'>Join DiabetesAI Pro</p>
            </div>
            """, unsafe_allow_html=True)

            rn = st.text_input("Full Name",        placeholder="Your full name",  key="rn")
            re = st.text_input("Email",             placeholder="Your email",      key="re")
            ru = st.text_input("Username",          placeholder="Choose username", key="ru")
            rp = st.text_input("Password",          placeholder="Min 6 chars",    type="password", key="rp")
            rp2= st.text_input("Confirm Password",  placeholder="Repeat password",type="password", key="rp2")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Create Account →"):
                if not all([rn,ru,rp,rp2]):
                    st.error("Please fill all required fields")
                elif rp != rp2:
                    st.error("Passwords do not match")
                elif len(rp) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    if add_user(ru, rp, rn, re):
                        st.success("✅ Account created! Please sign in.")
                        time.sleep(1)
                        st.session_state.auth_tab = "login"; st.rerun()
                    else:
                        st.error("Username already exists")
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# NAVIGATION
# ══════════════════════════════════════════════════════════
def show_nav():
    user  = st.session_state.user
    pages = ["Dashboard","Patient","Prediction","Records","Visualization","Health Tips"]
    if user["role"] == "admin": pages.append("Admin")

    st.markdown(f"""
    <div style='display:flex; align-items:center; justify-content:space-between;
                padding:14px 24px; background:var(--card);
                border-bottom:1px solid var(--border); margin-bottom:28px;
                position:sticky; top:0; z-index:100;'>
        <div style='display:flex; align-items:center; gap:10px;'>
            <span style='font-size:22px;'>🩺</span>
            <div style='font-family:"Playfair Display",serif; font-size:18px; font-weight:800; color:white;'>
                DiabetesAI <span style='color:#0fd4c8;'>Pro</span>
            </div>
        </div>
        <div style='display:flex; align-items:center; gap:8px;'>
            <span class='pulse-dot'></span>
            <span style='color:#5a7a9a; font-size:12px;'>
                {user['fullname']} · {user['role'].title()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(len(pages) + 1)
    icons = {"Dashboard":"🏠","Patient":"👤","Prediction":"🔬",
             "Records":"📋","Visualization":"📊","Health Tips":"💊","Admin":"⚙️"}

    for i, pg in enumerate(pages):
        with cols[i]:
            active = st.session_state.page == pg
            s = "background:rgba(15,212,200,0.15); border-color:rgba(15,212,200,0.4); color:#0fd4c8;" if active else ""
            st.markdown(f"""
            <div style='text-align:center; padding:10px 4px; border-radius:12px;
                        border:1px solid var(--border); {s} transition:all 0.2s; margin-bottom:4px;'>
                <div style='font-size:18px;'>{icons.get(pg,"●")}</div>
                <div style='font-size:9px; font-weight:600; text-transform:uppercase;
                            letter-spacing:0.8px; margin-top:3px;
                            color:{"#0fd4c8" if active else "#5a7a9a"};'>{pg}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(pg, key=f"nav_{pg}", use_container_width=True):
                st.session_state.page = pg; st.rerun()

    with cols[len(pages)]:
        st.markdown("""
        <div style='text-align:center; padding:10px 4px; border-radius:12px;
                    border:1px solid rgba(255,69,96,0.25);
                    background:rgba(255,69,96,0.06); margin-bottom:4px;'>
            <div style='font-size:18px;'>🚪</div>
            <div style='font-size:9px; font-weight:600; text-transform:uppercase;
                        letter-spacing:0.8px; margin-top:3px; color:#ff4560;'>Logout</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="nav_logout", use_container_width=True):
            for k in ["logged_in","user","page","last_result","sel_patient"]:
                st.session_state[k] = False if k == "logged_in" else None
            st.session_state.page = "Dashboard"
            st.rerun()

    st.markdown("<div style='height:1px; background:var(--border); margin-bottom:24px;'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════
def page_dashboard():
    user    = st.session_state.user
    records = get_user_records(user["username"])
    total   = len(records)
    df      = pd.DataFrame(records, columns=RECORD_COLS) if records else pd.DataFrame()

    diabetic = len(df[df["Result"]=="Diabetic"])  if not df.empty else 0
    healthy  = total - diabetic
    patients = get_patients(user["username"])

    st.markdown(f"""
    <div class='hero-header'>
        <div class='hero-title'>Good {("Morning" if datetime.now().hour < 12 else "Afternoon" if datetime.now().hour < 18 else "Evening")}, {user['fullname'].split()[0]} 👋</div>
        <p class='hero-sub'>Here's your diabetes prediction dashboard overview</p>
        <div style='margin-top:14px; font-size:12px; color:#5a7a9a;'>
            {datetime.now().strftime("%A, %d %B %Y")}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, num, lbl, col_str in [
        (c1, total,         "Total Predictions",  "#0fd4c8"),
        (c2, diabetic,      "Diabetic Cases",      "#ff4560"),
        (c3, healthy,       "Healthy Cases",       "#00e396"),
        (c4, len(patients), "Patients Registered", "#f0b429"),
    ]:
        with col:
            st.markdown(f"""
            <div class='stat-card'>
                <div class='stat-num' style='color:{col_str};'>{num}</div>
                <div class='stat-lbl'>{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("<div class='glass-card'><h4>📈 Recent Predictions</h4>", unsafe_allow_html=True)
        if not df.empty:
            recent = df.head(5)[["Name","Age","Glucose","BMI","Result","Probability","Date"]]
            st.dataframe(recent, use_container_width=True, hide_index=True)
        else:
            st.markdown("<p style='color:#5a7a9a; text-align:center; padding:20px;'>No predictions yet</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h4>📊 Case Distribution</h4>", unsafe_allow_html=True)
        if total > 0:
            fig = go.Figure(go.Pie(
                labels=["Diabetic","Healthy"],
                values=[diabetic, healthy],
                hole=0.6,
                marker=dict(colors=["#ff4560","#00e396"]),
                textinfo="percent",
                textfont=dict(family="Outfit", size=12, color="white"),
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(font=dict(color="white", family="Outfit", size=11)),
                margin=dict(t=10,b=10,l=10,r=10),
                height=220,
                annotations=[dict(text=str(total), x=0.5, y=0.5, font_size=22,
                                  font_color="white", showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.markdown("<p style='color:#5a7a9a; text-align:center; padding:20px;'>No data yet</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PATIENT REGISTRATION
# ══════════════════════════════════════════════════════════
def page_patient():
    user = st.session_state.user
    st.markdown("<div class='hero-header'><div class='hero-title'>👤 Patient Registration</div><p class='hero-sub'>Register new patients before prediction</p></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-card'><h4>➕ Register New Patient</h4>", unsafe_allow_html=True)
        p_name  = st.text_input("Patient Full Name",  placeholder="Enter full name",   key="pn")
        p_age   = st.number_input("Age",               min_value=1, max_value=120, value=30, key="pa")
        p_sex   = st.selectbox("Sex",                  ["Male","Female","Other"],        key="ps")
        p_phone = st.text_input("Phone Number",        placeholder="Optional",          key="pph")
        p_blood = st.selectbox("Blood Group",          ["A+","A-","B+","B-","O+","O-","AB+","AB-","Unknown"], key="pb")

        if st.button("💾 Register Patient"):
            if not p_name:
                st.error("Please enter patient name!")
            else:
                pid = save_patient(user["username"], p_name, p_age, p_sex, p_phone, p_blood)
                if pid:
                    st.success(f"✅ Patient registered! ID: **{pid}**")
                    st.session_state.sel_patient = pid
                    time.sleep(1); st.rerun()
                else:
                    st.error("Registration failed")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h4>📋 Registered Patients</h4>", unsafe_allow_html=True)
        patients = get_patients(user["username"])
        if patients:
            pdf = pd.DataFrame(patients, columns=["ID","PatientID","Username","Name","Age","Sex","Phone","BloodGrp","Created"])
            show = pdf[["PatientID","Name","Age","Sex","BloodGrp","Created"]]
            st.dataframe(show, use_container_width=True, hide_index=True)
        else:
            st.markdown("<p style='color:#5a7a9a; text-align:center; padding:20px;'>No patients yet</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PREDICTION
# ══════════════════════════════════════════════════════════
def page_prediction():
    user = st.session_state.user
    st.markdown("<div class='hero-header'><div class='hero-title'>🔬 Diabetes Prediction</div><p class='hero-sub'>Enter medical parameters to get instant prediction</p></div>", unsafe_allow_html=True)

    patients = get_patients(user["username"])

    if not patients:
        st.warning("⚠️ Please register a patient first in the Patient page!")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='glass-card'><h4>👤 Select Patient</h4>", unsafe_allow_html=True)
        patient_options = {f"{p[3]} ({p[1]})": p for p in patients}
        sel_label       = st.selectbox("Select Patient", list(patient_options.keys()))
        sel_p           = patient_options[sel_label]

        st.markdown(f"""
        <div class='patient-badge'>
            <b style='color:#0fd4c8;'>ID:</b> {sel_p[1]} &nbsp;|&nbsp;
            <b style='color:#0fd4c8;'>Age:</b> {sel_p[4]} &nbsp;|&nbsp;
            <b style='color:#0fd4c8;'>Sex:</b> {sel_p[5]} &nbsp;|&nbsp;
            <b style='color:#0fd4c8;'>Blood:</b> {sel_p[7]}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='glass-card'><h4>🩸 Blood Parameters</h4>", unsafe_allow_html=True)
        glucose = st.number_input("Glucose Level (mg/dL)",  0.0, 300.0, 100.0, 1.0, help="Normal: 70–140")
        insulin = st.number_input("Insulin Level (uU/mL)",  0.0, 900.0,  80.0, 1.0, help="Normal: 16–166")
        bp      = st.number_input("Blood Pressure (mmHg)",  0.0, 200.0,  70.0, 1.0, help="Normal: 60–90")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='glass-card'><h4>📊 Body Parameters</h4>", unsafe_allow_html=True)
        bmi = st.number_input("BMI (kg/m²)",                0.0,  70.0,  25.0, 0.1, help="Normal: 18.5–24.9")
        dpf = st.number_input("Diabetes Pedigree Function", 0.0,   3.0,   0.5, 0.001, format="%.3f")
        age = st.number_input("Age (years)",                1,    120,    sel_p[4], 1)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:rgba(15,212,200,0.05); border:1px solid rgba(15,212,200,0.12);
                    border-radius:12px; padding:16px; margin-bottom:16px;'>
            <div style='font-size:11px; color:#5a7a9a; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>Normal Ranges</div>
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:12px;'>
                <span style='color:#0fd4c8;'>Glucose:</span><span style='color:#e8f0f8;'>70–140 mg/dL</span>
                <span style='color:#0fd4c8;'>Insulin:</span><span style='color:#e8f0f8;'>16–166 uU/mL</span>
                <span style='color:#0fd4c8;'>BP:</span><span style='color:#e8f0f8;'>60–90 mmHg</span>
                <span style='color:#0fd4c8;'>BMI:</span><span style='color:#e8f0f8;'>18.5–24.9 kg/m²</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  PREDICT NOW"):
        if glucose <= 0 or bmi <= 0:
            st.error("Please enter valid medical values!")
            return

        features        = np.array([[glucose, bp, insulin, bmi, dpf, age]])
        features_scaled = scaler.transform(features)
        result          = int(model.predict(features_scaled)[0])
        prob            = round(float(model.predict_proba(features_scaled)[0][1]) * 100, 2)
        result_text     = "Diabetic" if result == 1 else "Non-Diabetic"
        risk_level      = get_risk_level(prob)
        recommendation  = get_recommendation(prob)

        add_record((user["username"], sel_p[1], sel_p[3], sel_p[4], sel_p[5],
                    glucose, bp, insulin, bmi, dpf,
                    result_text, prob, risk_level, recommendation,
                    datetime.now().strftime("%d/%m/%Y %H:%M")))

        st.session_state.last_result = {
            "name": sel_p[3], "patient_id": sel_p[1],
            "age": age, "sex": sel_p[5],
            "glucose": glucose, "bp": bp, "insulin": insulin,
            "bmi": bmi, "dpf": dpf,
            "result": result, "result_text": result_text,
            "prob": prob, "risk_level": risk_level, "recommendation": recommendation
        }

        st.markdown("<br>", unsafe_allow_html=True)
        r1, r2 = st.columns(2)

        with r1:
            cls = "danger" if result == 1 else "safe"
            emoji = "⚠️" if result == 1 else "✅"
            title = "DIABETIC" if result == 1 else "NOT DIABETIC"
            color = "#ff4560" if result == 1 else "#00e396"
            sub   = "High risk detected — Consult a doctor immediately" if result == 1 else "Low risk — Maintain healthy lifestyle"
            disp_prob = prob if result == 1 else round(100-prob, 2)

            st.markdown(f"""
            <div class='result-box {cls}'>
                <span class='result-emoji'>{emoji}</span>
                <div class='result-title'>{title}</div>
                <p style='color:{color}80; font-size:13px; margin-bottom:16px;'>{sub}</p>
                <div style='font-size:28px; font-weight:800; color:{color}; font-family:"Playfair Display",serif;'>{disp_prob}%</div>
                <div style='font-size:11px; color:#5a7a9a; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>Probability</div>
                <div class='prob-bar-bg'>
                    <div class='prob-bar-fill' style='width:{disp_prob}%;
                        background:{"linear-gradient(90deg,#ff4560,#ff8fa3)" if result==1 else "linear-gradient(90deg,#00e396,#69f0ae)"};'></div>
                </div>
                <div style='margin-top:12px;'>
                    <span style='font-size:12px; color:#5a7a9a;'>Risk Level: </span>
                    <b style='color:{color};'>{risk_level}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown("<div class='glass-card'><h4>⚡ Quick Risk Analysis</h4>", unsafe_allow_html=True)
            params = [
                ("Glucose", glucose, 70, 140, "mg/dL"),
                ("BMI",     bmi,    18.5, 24.9, "kg/m²"),
                ("Age",     age,    0,    45,   "yrs"),
                ("Insulin", insulin,16,  166,  "uU/mL"),
                ("BP",      bp,     60,   90,  "mmHg"),
                ("DPF",     dpf,    0,   0.8,  "score"),
            ]
            for nm, val, lo, hi, unit in params:
                abnormal = val < lo or val > hi
                tag = "risk-tag-high" if abnormal else "risk-tag-ok"
                icon = "⚠️" if abnormal else "✅"
                status = "Abnormal" if abnormal else "Normal"
                st.markdown(f"<div class='{tag}'>{icon} {nm}: <b>{val}</b> {unit} — {status}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='rec-box'>
            <h4>🩺 Health Recommendation</h4>
            <p style='font-size:14px; line-height:1.7;'>{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)

        st.success("✅ Prediction saved to database!")

# ══════════════════════════════════════════════════════════
# RECORDS
# ══════════════════════════════════════════════════════════
def page_records():
    user = st.session_state.user
    records = get_user_records(user["username"])

    st.markdown("<div class='hero-header'><div class='hero-title'>📋 Saved Records</div></div>", unsafe_allow_html=True)

    if not records:
        st.info("No records yet.")
        return

    df = pd.DataFrame(records, columns=RECORD_COLS)

    # Clean display (remove unnecessary columns)
    display_cols = ["PatientID","Name","Age","Sex","Glucose","BMI","BP","Result","Probability","RiskLevel","Date"]
    df_display = df[display_cols]

    # =========================
    # SHOW TABLE
    # =========================
    st.markdown("<div class='glass-card'><h4>📊 All Records</h4>", unsafe_allow_html=True)
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # DOWNLOAD ALL RECORDS
    # =========================
    if not df_display.empty:
        all_pdf = generate_pdf(
            title="All Patient Records",
            subtitle=f"User: {user['username']}",
            df=df_display
        )

        st.download_button(
            "📄 Download All Records",
            data=all_pdf,
            file_name="All_patient records.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # =========================
    # PATIENT-WISE DOWNLOAD
    # =========================
    st.markdown("<div class='glass-card'><h4>👤 Patient Report</h4>", unsafe_allow_html=True)

    patients = get_patients(user["username"])

    if not patients:
        st.warning("No patients found.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    p_opts = {f"{p[3]} ({p[1]})": p for p in patients}
    sel_label = st.selectbox("Select Patient", list(p_opts.keys()))
    sel_p = p_opts[sel_label]

    # Get patient records
    p_records = get_patient_records(user["username"], sel_p[1])

    if not p_records:
        st.warning("No records found for this patient")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    p_df = pd.DataFrame(p_records, columns=RECORD_COLS)
    p_df_display = p_df[display_cols]

    # Show patient records
    st.dataframe(p_df_display, use_container_width=True, hide_index=True)

    # Generate PDF
    p_pdf = generate_pdf(
        title=f"Patient Report - {sel_p[3]}",
        subtitle=f"Patient ID: {sel_p[1]}",
        df=p_df_display
    )

    st.download_button(
        "📄 Download Patient Report",
        data=p_pdf,
        file_name=f"{sel_p[1]}_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════
# VISUALIZATION
# ══════════════════════════════════════════════════════════
def page_visualization():
    user    = st.session_state.user
    records = get_user_records(user["username"])
    st.markdown("<div class='hero-header'><div class='hero-title'>📊 Data Visualization</div><p class='hero-sub'>Visual analytics of patient prediction data</p></div>", unsafe_allow_html=True)

    if not records:
        st.info("No records yet. Run predictions to view charts!"); return

    df = pd.DataFrame(records, columns=RECORD_COLS)

    chart_bg    = "rgba(0,0,0,0)"
    font_color  = "#e8f0f8"
    grid_color  = "rgba(15,212,200,0.08)"
    plot_layout = dict(
        paper_bgcolor=chart_bg, plot_bgcolor=chart_bg,
        font=dict(family="Outfit", color=font_color, size=12),
        margin=dict(t=20,b=20,l=10,r=10),
        xaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color),
        yaxis=dict(gridcolor=grid_color, zerolinecolor=grid_color),
        height=280,
    )

    # Row 1
    r1c1, r1c2, r1c3 = st.columns(3)

    with r1c1:
        st.markdown("<div class='glass-card'><h4>🥧 Result Distribution</h4>", unsafe_allow_html=True)
        counts = df["Result"].value_counts()
        fig    = go.Figure(go.Pie(
            labels=counts.index, values=counts.values, hole=0.55,
            marker=dict(colors=["#ff4560","#00e396"],
                        line=dict(color="#060d18", width=2)),
            textinfo="percent+label",
            textfont=dict(family="Outfit", size=11, color="white"),
        ))
        fig.update_layout(**{**plot_layout, "showlegend":False,
            "annotations":[dict(text=str(len(df)), x=0.5, y=0.5,
                               font_size=20, font_color="white", showarrow=False)]})
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    with r1c2:
        st.markdown("<div class='glass-card'><h4>🩸 Glucose by Patient</h4>", unsafe_allow_html=True)
        fig = px.bar(df, x="Name", y="Glucose",
                     color="Result",
                     color_discrete_map={"Diabetic":"#ff4560","Non-Diabetic":"#00e396"})
        fig.update_layout(**plot_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    with r1c3:
        st.markdown("<div class='glass-card'><h4>⚖️ BMI Distribution</h4>", unsafe_allow_html=True)
        fig = px.bar(df, x="Name", y="BMI",
                     color="Result",
                     color_discrete_map={"Diabetic":"#ff4560","Non-Diabetic":"#00e396"})
        fig.update_layout(**plot_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2
    r2c1, r2c2 = st.columns(2)

    with r2c1:
        st.markdown("<div class='glass-card'><h4>📈 Probability Score per Patient</h4>", unsafe_allow_html=True)
        fig = px.bar(df, x="Name", y="Probability",
                     color="Probability",
                     color_continuous_scale=["#00e396","#f0b429","#ff4560"],
                     range_color=[0,100])
        fig.update_layout(**{**plot_layout, "coloraxis_showscale":False, "height":300})
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    with r2c2:
        st.markdown("<div class='glass-card'><h4>📊 Multi-Parameter Trends</h4>", unsafe_allow_html=True)
        fig = go.Figure()
        for param, color in [("Glucose","#0fd4c8"),("BMI","#f0b429"),("BP","#ff4560")]:
            fig.add_trace(go.Scatter(
                x=df["Name"], y=df[param], mode="lines+markers",
                name=param,
                line=dict(color=color, width=2),
                marker=dict(size=6, color=color)
            ))
        fig.update_layout(**{**plot_layout, "height":300,
                              "legend":dict(font=dict(color="white", family="Outfit"))})
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 3 — Last prediction radar
    if st.session_state.last_result:
        r = st.session_state.last_result
        st.markdown("<div class='glass-card'><h4>🎯 Last Prediction — Parameter Radar</h4>", unsafe_allow_html=True)
        categories = ["Glucose","BP","Insulin","BMI","DPF"]
        normals    = [140, 90, 166, 24.9, 0.8]
        values     = [r["glucose"], r["bp"], r["insulin"], r["bmi"], r["dpf"]]
        normalized = [min(v/n, 2) for v,n in zip(values, normals)]

        fig = go.Figure(go.Scatterpolar(
            r=normalized + [normalized[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(15,212,200,0.15)",
            line=dict(color="#0fd4c8", width=2),
            marker=dict(color="#0fd4c8", size=6),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,2],
                                gridcolor="rgba(15,212,200,0.15)",
                                tickfont=dict(color="#5a7a9a")),
                angularaxis=dict(gridcolor="rgba(15,212,200,0.1)",
                                 tickfont=dict(color=font_color, family="Outfit"))
            ),
            font=dict(family="Outfit", color=font_color),
            margin=dict(t=20,b=20,l=40,r=40),
            height=300, showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# HEALTH TIPS
# ══════════════════════════════════════════════════════════
def page_health_tips():
    last = st.session_state.last_result
    st.markdown("<div class='hero-header'><div class='hero-title'>💊 Health Recommendations</div><p class='hero-sub'>Personalized health tips based on prediction result</p></div>", unsafe_allow_html=True)

    if last:
        risk = last["risk_level"]
        col = "#ff4560" if risk == "HIGH" else "#f0b429" if risk == "MODERATE" else "#00e396"
        st.markdown(f"""
        <div style='background:rgba(15,212,200,0.05); border:1px solid rgba(15,212,200,0.15); border-radius:14px; padding:18px 24px; margin-bottom:24px;'>
            <p style='margin:0; font-size:14px;'>
            Last result: <b style='color:white;'>{last["name"]}</b> &nbsp;|&nbsp;
            Result: <b style='color:{col};'>{last["result_text"]}</b> &nbsp;|&nbsp;
            Risk: <b style='color:{col};'>{risk}</b> &nbsp;|&nbsp;
            Probability: <b style='color:{col};'>{last["prob"]}%</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='glass-card'>
            <h4>🥗 Diet Recommendations</h4>
            <ul style='line-height:2.2; padding-left:18px; font-size:13px;'>
                <li>Avoid sugary drinks, sweets and desserts</li>
                <li>Eat more green vegetables and fresh fruits</li>
                <li>Choose whole grains — brown rice, wheat bread</li>
                <li>Limit white rice, white bread and fried foods</li>
                <li>Drink 8 to 10 glasses of water daily</li>
                <li>Eat small meals every 3 to 4 hours</li>
                <li>Avoid processed and packaged foods</li>
                <li>Include fiber rich foods in daily diet</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card'>
            <h4>🏃 Exercise & Activity</h4>
            <ul style='line-height:2.2; padding-left:18px; font-size:13px;'>
                <li>Walk briskly for at least 30 minutes daily</li>
                <li>Do light exercises 5 days a week</li>
                <li>Try yoga, swimming or cycling</li>
                <li>Avoid sitting for more than 1 hour continuously</li>
                <li>Maintain healthy body weight (BMI 18.5–24.9)</li>
                <li>Do stretching exercises every morning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='glass-card'>
            <h4>🏥 Medical Advice</h4>
            <ul style='line-height:2.2; padding-left:18px; font-size:13px;'>
                <li>Consult a doctor immediately if high risk</li>
                <li>Check blood sugar levels every 3 months</li>
                <li>Monitor blood pressure every week</li>
                <li>Get HbA1c test done every 3 months</li>
                <li>Take prescribed medicines regularly</li>
                <li>Never skip doctor appointments</li>
                <li>Get eye and kidney checkup annually</li>
                <li>Monitor cholesterol and lipid levels</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='glass-card'>
            <h4>😴 Lifestyle & Mental Health</h4>
            <ul style='line-height:2.2; padding-left:18px; font-size:13px;'>
                <li>Sleep 7 to 8 hours every night</li>
                <li>Completely avoid smoking and alcohol</li>
                <li>Practice meditation to manage stress</li>
                <li>Track daily food and water intake</li>
                <li>Stay positive and mentally healthy</li>
                <li>Reduce screen time before sleep</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Risk levels guide
    st.markdown("<div class='glass-card'><h4>🎯 Risk Level Guide</h4>", unsafe_allow_html=True)
    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.markdown("""
        <div style='background:rgba(255,69,96,0.08); border:1px solid rgba(255,69,96,0.2); border-radius:12px; padding:18px; text-align:center;'>
            <div style='font-size:28px; color:#ff4560; font-weight:800; font-family:"Playfair Display",serif;'>HIGH</div>
            <div style='font-size:12px; color:#5a7a9a; margin:6px 0;'>Probability ≥ 70%</div>
            <div style='font-size:13px; color:#e8f0f8;'>Consult doctor immediately. Strict medical supervision required.</div>
        </div>""", unsafe_allow_html=True)
    with rc2:
        st.markdown("""
        <div style='background:rgba(240,180,41,0.08); border:1px solid rgba(240,180,41,0.2); border-radius:12px; padding:18px; text-align:center;'>
            <div style='font-size:28px; color:#f0b429; font-weight:800; font-family:"Playfair Display",serif;'>MODERATE</div>
            <div style='font-size:12px; color:#5a7a9a; margin:6px 0;'>Probability 40–70%</div>
            <div style='font-size:13px; color:#e8f0f8;'>Lifestyle changes needed. Regular monitoring advised.</div>
        </div>""", unsafe_allow_html=True)
    with rc3:
        st.markdown("""
        <div style='background:rgba(0,227,150,0.08); border:1px solid rgba(0,227,150,0.2); border-radius:12px; padding:18px; text-align:center;'>
            <div style='font-size:28px; color:#00e396; font-weight:800; font-family:"Playfair Display",serif;'>LOW</div>
            <div style='font-size:12px; color:#5a7a9a; margin:6px 0;'>Probability &lt; 40%</div>
            <div style='font-size:13px; color:#e8f0f8;'>Maintain healthy habits. Routine checkups sufficient.</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════
def page_admin():
    st.markdown("<div class='hero-header'><div class='hero-title'>⚙️ Admin Panel</div><p class='hero-sub'>System administration and management</p></div>", unsafe_allow_html=True)

    users   = get_all_users()
    records = get_all_records()

    u_df = pd.DataFrame(users,   columns=["ID","Username","Full Name","Email","Role","Joined"]) if users else pd.DataFrame()
    r_df = pd.DataFrame(records, columns=RECORD_COLS) if records else pd.DataFrame()

    total    = len(r_df)
    diabetic = len(r_df[r_df["Result"]=="Diabetic"]) if not r_df.empty else 0

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(f"<div class='stat-card'><div class='stat-num'>{len(users)}</div><div class='stat-lbl'>Total Users</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'><div class='stat-num'>{total}</div><div class='stat-lbl'>Total Records</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><div class='stat-num' style='color:#ff4560;'>{diabetic}</div><div class='stat-lbl'>Diabetic</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='stat-card'><div class='stat-num' style='color:#00e396;'>{total-diabetic}</div><div class='stat-lbl'>Not Diabetic</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'><h4>👥 Registered Users</h4>", unsafe_allow_html=True)
    if not u_df.empty: st.dataframe(u_df, use_container_width=True, hide_index=True)
    else: st.info("No users found")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'><h4>📋 All Patient Records</h4>", unsafe_allow_html=True)
    if not r_df.empty:
        show = r_df.drop(columns=["ID"], errors="ignore")
        st.dataframe(show, use_container_width=True, hide_index=True)

        admin_pdf = generate_pdf("All Patients (Admin)", "ADMIN-ALL", r_df)
        st.download_button(
            "📄 Download All Records PDF",
            data=admin_pdf,
            file_name=f"admin_all_records_{datetime.now().strftime('%d%m%Y')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.info("No records found")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN FLOW
# ══════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_auth()
else:
    show_nav()
    page = st.session_state.page
    if page == "Dashboard":    page_dashboard()
    elif page == "Patient":    page_patient()
    elif page == "Prediction": page_prediction()
    elif page == "Records":    page_records()
    elif page == "Visualization": page_visualization()
    elif page == "Health Tips":   page_health_tips()
    elif page == "Admin" and st.session_state.user["role"] == "admin": page_admin()

