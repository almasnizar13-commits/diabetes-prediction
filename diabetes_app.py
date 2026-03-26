import streamlit as st
import sqlite3
import pandas as pd
import pickle
from datetime import datetime
import numpy as np

# ══════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════
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
[data-baseweb="popover"], [data-baseweb="menu"] { background: #ffffff !important; }
[data-baseweb="popover"] li, [data-baseweb="menu"] li {
    color: #000000 !important;
    background: #ffffff !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-baseweb="popover"] li:hover, [data-baseweb="menu"] li:hover {
    background: #e6f9f9 !important;
    color: #005f73 !important;
}

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

.auth-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px; padding: 44px 40px;
    max-width: 440px; margin: 0 auto;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

.metric-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px; padding: 18px; text-align: center;
}
.metric-card h3 { color: #94d2bd !important; font-size: 24px; font-weight: 700; margin:0; }
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

# ══════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════
conn = sqlite3.connect("diabetes.db", check_same_thread=False)
c    = conn.cursor()

def create_tables():
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id             INTEGER PRIMARY KEY,
            username       TEXT,
            name           TEXT,
            age            INTEGER,
            gender         TEXT,
            glucose        REAL,
            bp             REAL,
            insulin        REAL,
            bmi            REAL,
            dpf            REAL,
            result         TEXT,
            probability    REAL,
            recommendation TEXT,
            date           TEXT
        )
    """)
    # Default admin
    c.execute("INSERT OR IGNORE INTO users (username, password,) VALUES (?,?)",
              ("admin", "admin123"))
    conn.commit()

create_tables()

def add_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                  (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

def add_record(data):
    c.execute("""
        INSERT INTO records
        (username, name, age, gender, glucose, bp, insulin, bmi, dpf,
         result, probability, recommendation, date)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, data)
    conn.commit()

def get_all_records():
    c.execute("SELECT * FROM records ORDER BY id DESC")
    return c.fetchall()

def get_user_records(username):
    c.execute("SELECT * FROM records WHERE username=? ORDER BY id DESC", (username,))
    return c.fetchall()

def get_patient_names(username):
    c.execute("SELECT DISTINCT name FROM records WHERE username=?", (username,))
    return [row[0] for row in c.fetchall()]

def get_patient_records(username, name):
    c.execute("SELECT * FROM records WHERE username=? AND name=? ORDER BY id DESC",
              (username, name))
    return c.fetchall()

# ══════════════════════════════════════════════════════════
# MODEL
# ══════════════════════════════════════════════════════════
model  = pickle.load(open("diabetes_svm_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
if "login"    not in st.session_state: st.session_state.login    = False
if "username" not in st.session_state: st.session_state.username = ""
if "fullname" not in st.session_state: st.session_state.fullname = ""
if "page"     not in st.session_state: st.session_state.page     = "Prediction"
if "last_result" not in st.session_state: st.session_state.last_result = None

# ══════════════════════════════════════════════════════════
# RECOMMENDATION
# ══════════════════════════════════════════════════════════
def get_recommendation(prob):
    if prob >= 70:
        return "HIGH RISK: Consult doctor immediately, strict diet, daily exercise, check blood sugar regularly"
    elif prob >= 40:
        return "MODERATE RISK: Control diet, exercise regularly, monitor blood sugar monthly"
    else:
        return "LOW RISK: Maintain healthy lifestyle, regular checkups, stay active"

# ══════════════════════════════════════════════════════════
# COLUMNS HELPER
# ══════════════════════════════════════════════════════════
COLS = ["ID","Username","Name","Age","Gender","Glucose","BP",
        "Insulin","BMI","DPF","Result","Probability","Recommendation","Date"]

# ══════════════════════════════════════════════════════════
# LOGIN / REGISTER PAGE
# ══════════════════════════════════════════════════════════
def auth_page():
    st.markdown("""
    <div style='text-align:center; padding:36px 0 16px;'>
        <div style='font-size:52px;'>🩺</div>
        <h1 style='color:white !important; font-size:30px; font-weight:700; margin:8px 0 4px;'>Diabetes Prediction</h1>
        <p style='color:rgba(255,255,255,0.5) !important; font-size:13px;'>Smart Diabetes Prediction </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:

        if "auth_tab" not in st.session_state:
            st.session_state.auth_tab = "login"

        tab1, tab2 = st.columns(2)
        with tab1:
            if st.button("🔐 Login",    key="tab_login"):
                st.session_state.auth_tab = "login"
                st.rerun()
        with tab2:
            if st.button("📝 Register", key="tab_reg"):
                st.session_state.auth_tab = "register"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── LOGIN ──────────────────────────────────────────
        if st.session_state.auth_tab == "login":
            st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:white !important; text-align:center; margin-bottom:4px;'>Welcome Back 👋</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color:rgba(255,255,255,0.5) !important; text-align:center; font-size:12px; margin-bottom:20px;'>Login to access the system</p>", unsafe_allow_html=True)

            username = st.text_input("👤 Username", placeholder="Enter username", key="l_user")
            password = st.text_input("🔒 Password", placeholder="Enter password", type="password", key="l_pass")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔐 LOGIN"):
                if username == "" or password == "":
                    st.error("⚠️ Please enter username and password!")
                else:
                    user = login_user(username, password)
                    if user:
                        st.session_state.login    = True
                        st.session_state.username = user[1]
                        st.session_state.fullname = user[3]
                        st.session_state.page     = "Prediction"
                        # ✅ Show success then redirect
                        success_placeholder = st.empty()
                        success_placeholder.success(f"✅ Login Successful! Welcome {user[3]}!")
                        import time
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Wrong username or password!")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background:rgba(10,147,150,0.1); border:1px solid rgba(10,147,150,0.3); border-radius:10px; padding:10px; text-align:center;'>
                <p style='color:rgba(255,255,255,0.7) !important; font-size:12px; margin:0;'>
                🔑 Admin: <b style='color:#94d2bd;'>admin</b> / <b style='color:#94d2bd;'>admin123</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── REGISTER ──────────────────────────────────────
        else:
            st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:white !important; text-align:center; margin-bottom:4px;'>Create Account 📝</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color:rgba(255,255,255,0.5) !important; text-align:center; font-size:12px; margin-bottom:20px;'>Register to get started</p>", unsafe_allow_html=True)

            reg_name  = st.text_input("👤 Full Name",        placeholder="Enter full name",    key="r_name")
            reg_user  = st.text_input("🆔 Username",         placeholder="Choose username",     key="r_user")
            reg_pass  = st.text_input("🔒 Password",         placeholder="Choose password",     type="password", key="r_pass")
            reg_pass2 = st.text_input("🔒 Confirm Password", placeholder="Confirm password",    type="password", key="r_pass2")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("📝 CREATE ACCOUNT"):
                if reg_name == "" or reg_user == "" or reg_pass == "":
                    st.error("⚠️ Please fill all fields!")
                elif reg_pass != reg_pass2:
                    st.error("❌ Passwords do not match!")
                elif len(reg_pass) < 6:
                    st.error("⚠️ Password must be at least 6 characters!")
                else:
                    if add_user(reg_user, reg_pass, reg_name):
                        st.success("✅ Account created successfully! Please login.")
                        import time
                        time.sleep(1)
                        st.session_state.auth_tab = "login"
                        st.rerun()
                    else:
                        st.error("❌ Username already exists! Try another.")
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════
def main_app():
    username = st.session_state.username
    fullname = st.session_state.fullname

    # ── TOP HEADER ──────────────────────────────────────
    st.markdown(f"""
    <div style='text-align:center; padding:12px 0 6px;'>
        <span style='font-size:28px;'>🩺</span>
        <h2 style='color:white !important; font-weight:700; margin:4px 0 2px;'>DiabetesAI</h2>
        <p style='color:rgba(255,255,255,0.45) !important; font-size:11px;'>Welcome, <b style='color:#94d2bd;'>{fullname}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # ── NAVIGATION ──────────────────────────────────────
    pages = [("🔬","Prediction"), ("📂","History"), ("📊","Visualization")]
    if username == "admin":
        pages.append(("⚙️","Admin"))

    cols = st.columns(len(pages) + 1)

    for i, (icon, label) in enumerate(pages):
        with cols[i]:
            selected = st.session_state.page == label
            style    = "background:rgba(10,147,150,0.3); border:1.5px solid #0a9396;" if selected else "background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1);"
            st.markdown(f"""
            <div style='{style} border-radius:14px; padding:12px 6px; text-align:center; margin-bottom:4px;'>
                <div style='font-size:22px;'>{icon}</div>
                <div style='font-size:9px; color:rgba(255,255,255,0.8); font-weight:500; text-transform:uppercase; letter-spacing:0.8px; margin-top:4px;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.session_state.page = label
                st.rerun()

    with cols[len(pages)]:
        st.markdown("""
        <div style='background:rgba(230,57,70,0.1); border:1px solid rgba(230,57,70,0.3); border-radius:14px; padding:12px 6px; text-align:center; margin-bottom:4px;'>
            <div style='font-size:22px;'>🚪</div>
            <div style='font-size:9px; color:rgba(230,57,70,0.9); font-weight:500; text-transform:uppercase; letter-spacing:0.8px; margin-top:4px;'>Logout</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.login       = False
            st.session_state.username    = ""
            st.session_state.fullname    = ""
            st.session_state.last_result = None
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.07); margin:6px 0 20px;'>", unsafe_allow_html=True)

    page = st.session_state.page

    # ════════════════════════════════════════════════════
    # PREDICTION PAGE
    # ════════════════════════════════════════════════════
    if page == "Prediction":
        st.markdown("""
        <div class='header-box'>
            <h1>🔬 Diabetes Prediction</h1>
            <p>Enter patient details to get instant prediction</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='card'><h4>👤 Patient Information</h4>", unsafe_allow_html=True)
            name   = st.text_input("Full Name",    placeholder="Enter patient name")
            age    = st.number_input("Age",         min_value=1,   max_value=120,  value=30,  step=1)
            gender = st.selectbox("Gender",         ["Male", "Female", "Other"])
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'><h4>🩸 Medical Parameters</h4>", unsafe_allow_html=True)
            glucose = st.number_input("Glucose (mg/dL)",           min_value=0.0, max_value=300.0, value=100.0, step=1.0,   help="Normal: 70–140")
            bp      = st.number_input("Blood Pressure (mmHg)",     min_value=0.0, max_value=200.0, value=70.0,  step=1.0,   help="Normal: 60–90")
            insulin = st.number_input("Insulin (μU/mL)",           min_value=0.0, max_value=900.0, value=80.0,  step=1.0,   help="Normal: 16–166")
            bmi     = st.number_input("BMI (kg/m²)",               min_value=0.0, max_value=70.0,  value=25.0,  step=0.1,   help="Normal: 18.5–24.9")
            dpf     = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0,   value=0.5,   step=0.001, format="%.3f")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("⚡ PREDICT NOW"):
            if name == "":
                st.error("⚠️ Please enter patient name!")
            elif glucose <= 0 or bp <= 0 or bmi <= 0:
                st.error("❌ Please enter valid medical values!")
            else:
                features        = np.array([[glucose, bp, insulin, bmi, dpf, age]])
                features_scaled = scaler.transform(features)
                result          = int(model.predict(features_scaled)[0])
                prob            = round(float(model.predict_proba(features_scaled)[0][1]) * 100, 2)
                result_text     = "Diabetic" if result == 1 else "Non-Diabetic"
                recommendation  = get_recommendation(prob)

                # Save to DB
                add_record((username, name, age, gender, glucose, bp,
                            insulin, bmi, dpf, result_text, prob,
                            recommendation, datetime.now().strftime("%d/%m/%Y %H:%M")))

                # Store result
                st.session_state.last_result = {
                    "name": name, "age": age, "gender": gender,
                    "glucose": glucose, "bp": bp, "insulin": insulin,
                    "bmi": bmi, "dpf": dpf,
                    "result": result, "result_text": result_text,
                    "prob": prob, "recommendation": recommendation
                }

                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)

                with col1:
                    if result == 1:
                        st.markdown(f"""
                        <div class='result-diabetic'>
                            <div style='font-size:48px;'>⚠️</div>
                            <h2>DIABETIC</h2>
                            <p style='font-size:14px; margin:8px 0;'>High diabetes risk detected</p>
                            <p style='font-size:13px;'>Probability: <b>{prob}%</b></p>
                            <div style='background:rgba(0,0,0,0.1); border-radius:100px; height:10px; margin:10px 0; overflow:hidden;'>
                                <div style='width:{prob}%; height:100%; background:linear-gradient(90deg,#e63946,#ff8fa3); border-radius:100px;'></div>
                            </div>
                            <p style='font-size:12px;'>⚠️ Please consult a doctor immediately</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        hp = round(100 - prob, 2)
                        st.markdown(f"""
                        <div class='result-healthy'>
                            <div style='font-size:48px;'>✅</div>
                            <h2>NOT DIABETIC</h2>
                            <p style='font-size:14px; margin:8px 0;'>Low diabetes risk detected</p>
                            <p style='font-size:13px;'>Healthy Probability: <b>{hp}%</b></p>
                            <div style='background:rgba(0,0,0,0.1); border-radius:100px; height:10px; margin:10px 0; overflow:hidden;'>
                                <div style='width:{hp}%; height:100%; background:linear-gradient(90deg,#2dc653,#69f0ae); border-radius:100px;'></div>
                            </div>
                            <p style='font-size:12px;'>✅ Maintain your healthy lifestyle!</p>
                        </div>
                        """, unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='card'><h4>⚡ Quick Risk Check</h4>", unsafe_allow_html=True)
                    for n_r, val, low, high, unit in [
                        ("🩸 Glucose", glucose, 70,   140,  "mg/dL"),
                        ("⚖️ BMI",     bmi,     18.5, 24.9, "kg/m²"),
                        ("🎂 Age",     age,     0,    45,   "yrs"),
                        ("💉 Insulin", insulin, 16,   166,  "μU/mL"),
                        ("🫀 BP",      bp,      60,   90,   "mmHg"),
                    ]:
                        if val < low or val > high:
                            st.markdown(f"<div class='risk-high'>⚠️ {n_r}: {val} {unit} — Abnormal</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='risk-ok'>✅ {n_r}: {val} {unit} — Normal</div>",     unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # ── RECOMMENDATION BOX ──────────────────
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background:rgba(10,147,150,0.1); border:1px solid rgba(10,147,150,0.4); border-radius:12px; padding:18px;'>
                    <h4 style='color:#94d2bd !important; margin-bottom:8px;'>🩺 Health Recommendation</h4>
                    <p style='color:rgba(255,255,255,0.85) !important; font-size:14px; margin:0;'>{recommendation}</p>
                </div>
                """, unsafe_allow_html=True)

                st.success("✅ Record saved to database!")

    # ════════════════════════════════════════════════════
    # HISTORY PAGE
    # ════════════════════════════════════════════════════
    elif page == "History":
        st.markdown("""
        <div class='header-box'>
            <h1>📂 Patient History</h1>
            <p>View and download patient records</p>
        </div>
        """, unsafe_allow_html=True)

        records = get_user_records(username)
        total   = len(records)

        if total == 0:
            st.info("📭 No records yet. Run a prediction to save records!")
        else:
            df = pd.DataFrame(records, columns=COLS)

            diabetic = len(df[df["Result"] == "Diabetic"])
            healthy  = total - diabetic

            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f"<div class='metric-card'><h3>{total}</h3><p>Total Records</p></div>",                                              unsafe_allow_html=True)
            with col2: st.markdown(f"<div class='metric-card'><h3 style='color:#ff6b6b !important;'>{diabetic}</h3><p>Diabetic</p></div>",              unsafe_allow_html=True)
            with col3: st.markdown(f"<div class='metric-card'><h3 style='color:#2dc653 !important;'>{healthy}</h3><p>Not Diabetic</p></div>",           unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── FILTER ──────────────────────────────────
            st.markdown("<div class='card'><h4>🔍 Filter Records</h4>", unsafe_allow_html=True)
            filter_opt = st.selectbox("Filter by", ["All Records", "Diabetic Only", "Non-Diabetic Only"])
            st.markdown("</div>", unsafe_allow_html=True)

            if filter_opt == "Diabetic Only":
                df = df[df["Result"] == "Diabetic"]
            elif filter_opt == "Non-Diabetic Only":
                df = df[df["Result"] == "Non-Diabetic"]

            # ── SHOW ALL RECORDS ─────────────────────────
            st.markdown("<div class='card'><h4>📋 All Records</h4>", unsafe_allow_html=True)
            show_df = df.drop(columns=["ID","Username"], errors='ignore')
            st.dataframe(show_df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── DOWNLOAD ALL ─────────────────────────────
            st.download_button(
                label="📥 DOWNLOAD ALL RECORDS (CSV)",
                data=df.to_csv(index=False),
                file_name=f"all_records_{datetime.now().strftime('%d%m%Y')}.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── DOWNLOAD SPECIFIC PATIENT ────────────────
            st.markdown("<div class='card'><h4>👤 Download Specific Patient Record</h4>", unsafe_allow_html=True)
            patient_names = get_patient_names(username)

            if patient_names:
                selected_patient = st.selectbox("Select Patient", patient_names)

                if selected_patient:
                    patient_records  = get_patient_records(username, selected_patient)
                    patient_df       = pd.DataFrame(patient_records, columns=COLS)
                    patient_df_show  = patient_df.drop(columns=["ID","Username"], errors='ignore')

                    st.markdown(f"<p style='color:rgba(255,255,255,0.8) !important;'>Found <b style='color:#94d2bd;'>{len(patient_df)}</b> records for <b style='color:#94d2bd;'>{selected_patient}</b></p>", unsafe_allow_html=True)
                    st.dataframe(patient_df_show, use_container_width=True)

                    # Generate text report for patient
                    report_lines = []
                    report_lines.append("=" * 55)
                    report_lines.append(f"  PATIENT HEALTH REPORT — {selected_patient.upper()}")
                    report_lines.append("=" * 55)
                    report_lines.append(f"Generated : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                    report_lines.append(f"Patient   : {selected_patient}")
                    report_lines.append(f"Records   : {len(patient_df)}")
                    report_lines.append("=" * 55)

                    for _, row in patient_df.iterrows():
                        report_lines.append(f"\nDate       : {row['Date']}")
                        report_lines.append(f"Age        : {row['Age']}")
                        report_lines.append(f"Gender     : {row['Gender']}")
                        report_lines.append(f"Glucose    : {row['Glucose']} mg/dL")
                        report_lines.append(f"BP         : {row['BP']} mmHg")
                        report_lines.append(f"Insulin    : {row['Insulin']} μU/mL")
                        report_lines.append(f"BMI        : {row['BMI']} kg/m²")
                        report_lines.append(f"DPF        : {row['DPF']}")
                        report_lines.append(f"Result     : {row['Result']}")
                        report_lines.append(f"Probability: {row['Probability']}%")
                        report_lines.append(f"Advice     : {row['Recommendation']}")
                        report_lines.append("-" * 40)

                    report_lines.append("\nDiabetesAI — Diabetes Prediction & Health Management System")
                    report_lines.append("For educational purposes only.")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label=f"📥 Download {selected_patient} CSV",
                            data=patient_df_show.to_csv(index=False),
                            file_name=f"{selected_patient.replace(' ','_')}_record.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    with col2:
                        st.download_button(
                            label=f"📄 Download {selected_patient} Report",
                            data="\n".join(report_lines),
                            file_name=f"{selected_patient.replace(' ','_')}_report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
            st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # VISUALIZATION PAGE
    # ════════════════════════════════════════════════════
    elif page == "Visualization":
        st.markdown("""
        <div class='header-box'>
            <h1>📊 Data Visualization</h1>
            <p>Visual analysis of patient records</p>
        </div>
        """, unsafe_allow_html=True)

        records = get_user_records(username)

        if not records:
            st.info("📭 No records yet. Run a prediction to view charts!")
        else:
            df = pd.DataFrame(records, columns=COLS)

            # ── CHART 1: Result Distribution ─────────────
            st.markdown("<div class='card'><h4>🥧 Diabetic vs Non-Diabetic Distribution</h4>", unsafe_allow_html=True)
            result_counts = df["Result"].value_counts().reset_index()
            result_counts.columns = ["Result", "Count"]
            st.bar_chart(result_counts.set_index("Result"))
            st.markdown("</div>", unsafe_allow_html=True)

            # ── CHART 2: Glucose Distribution ────────────
            st.markdown("<div class='card'><h4>🩸 Glucose Level Distribution</h4>", unsafe_allow_html=True)
            st.bar_chart(df[["Name","Glucose"]].set_index("Name"))
            st.markdown("</div>", unsafe_allow_html=True)

            # ── CHART 3: BMI Distribution ─────────────────
            st.markdown("<div class='card'><h4>⚖️ BMI Distribution</h4>", unsafe_allow_html=True)
            st.bar_chart(df[["Name","BMI"]].set_index("Name"))
            st.markdown("</div>", unsafe_allow_html=True)

            # ── CHART 4: Probability Distribution ────────
            st.markdown("<div class='card'><h4>📈 Diabetes Probability per Patient</h4>", unsafe_allow_html=True)
            st.bar_chart(df[["Name","Probability"]].set_index("Name"))
            st.markdown("</div>", unsafe_allow_html=True)

            # ── CHART 5: All Parameters ───────────────────
            st.markdown("<div class='card'><h4>📊 All Medical Parameters Comparison</h4>", unsafe_allow_html=True)
            params_df = df[["Name","Glucose","BP","Insulin","BMI"]].set_index("Name")
            st.line_chart(params_df)
            st.markdown("</div>", unsafe_allow_html=True)

            # ── CHART 6: Last Prediction ──────────────────
            if st.session_state.last_result:
                r = st.session_state.last_result
                st.markdown("<div class='card'><h4>🔬 Last Prediction — Parameter Chart</h4>", unsafe_allow_html=True)
                last_df = pd.DataFrame({
                    "Parameter": ["Glucose", "Blood Pressure", "Insulin", "BMI"],
                    "Value":     [r["glucose"], r["bp"], r["insulin"], r["bmi"]],
                    "Normal Max":[140, 90, 166, 24.9]
                })
                st.bar_chart(last_df.set_index("Parameter"))
                st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════
    # ADMIN PAGE
    # ════════════════════════════════════════════════════
    elif page == "Admin" and username == "admin":
        st.markdown("""
        <div class='header-box'>
            <h1>⚙️ Admin Panel</h1>
            <p>View and manage all users and records</p>
        </div>
        """, unsafe_allow_html=True)

        # All Users
        st.markdown("<div class='card'><h4>👥 All Registered Users</h4>", unsafe_allow_html=True)
        c.execute("SELECT id, username, fullname FROM users")
        users_data = c.fetchall()
        if users_data:
            users_df = pd.DataFrame(users_data, columns=["ID","Username","Full Name"])
            st.dataframe(users_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # All Records
        st.markdown("<div class='card'><h4>📋 All Patient Records</h4>", unsafe_allow_html=True)
        all_records = get_all_records()
        if all_records:
            all_df      = pd.DataFrame(all_records, columns=COLS)
            st.dataframe(all_df, use_container_width=True)

            total_all    = len(all_df)
            diabetic_all = len(all_df[all_df["Result"] == "Diabetic"])
            healthy_all  = total_all - diabetic_all

            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f"<div class='metric-card'><h3>{total_all}</h3><p>Total</p></div>",                                              unsafe_allow_html=True)
            with col2: st.markdown(f"<div class='metric-card'><h3 style='color:#ff6b6b !important;'>{diabetic_all}</h3><p>Diabetic</p></div>",      unsafe_allow_html=True)
            with col3: st.markdown(f"<div class='metric-card'><h3 style='color:#2dc653 !important;'>{healthy_all}</h3><p>Not Diabetic</p></div>",   unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 DOWNLOAD ALL RECORDS",
                data=all_df.to_csv(index=False),
                file_name=f"all_patients_{datetime.now().strftime('%d%m%Y')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No records found.")
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# FLOW
# ══════════════════════════════════════════════════════════
if st.session_state.login:
    main_app()
else:
    auth_page()
