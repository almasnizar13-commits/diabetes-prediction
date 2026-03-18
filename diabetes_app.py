
import streamlit as st
import numpy as np
import pickle

model  = pickle.load(open("diabetes_rf_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a3a4a 100%);
}

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}

label {
    color: #ffffff !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

p {
    color: rgba(255,255,255,0.85) !important;
}

li {
    color: rgba(255,255,255,0.80) !important;
}

.stNumberInput input {
    background: #ffffff !important;
    color: #000000 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    border: 2px solid #0a9396 !important;
    border-radius: 8px !important;
}

.stTextInput input {
    background: #ffffff !important;
    color: #000000 !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border: 2px solid #0a9396 !important;
    border-radius: 8px !important;
}

.stNumberInput input:focus,
.stTextInput input:focus {
    border-color: #94d2bd !important;
    box-shadow: 0 0 0 3px rgba(10,147,150,0.25) !important;
}

.header-box {
    background: linear-gradient(135deg, #0a9396, #005f73);
    border-radius: 16px;
    padding: 30px 40px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.header-box h1 { color: white !important; font-size: 32px; font-weight: 700; margin:0; }
.header-box p  { color: rgba(255,255,255,0.85) !important; font-size: 14px; margin:8px 0 0; }

.input-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 16px;
}
.input-card h3,
.input-card h4 {
    color: #94d2bd !important;
    margin-bottom: 14px;
}

.home-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
    text-align: center;
}
.home-card .icon { font-size: 40px; margin-bottom: 14px; display: block; }
.home-card h4    { color: #94d2bd !important; font-size: 17px; margin-bottom: 10px; }
.home-card p     { color: rgba(255,255,255,0.75) !important; font-size: 13px; line-height: 1.8; }

.login-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 48px 40px;
    max-width: 420px;
    margin: 0 auto;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

.result-diabetic {
    background: linear-gradient(135deg, #ffe5e7, #ffc4c7);
    border: 2px solid #e63946;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
}
.result-healthy {
    background: linear-gradient(135deg, #e6f9ed, #c8f5d8);
    border: 2px solid #2dc653;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
}
.result-diabetic h2 { color: #e63946 !important; font-size: 28px; font-weight: 700; }
.result-healthy  h2 { color: #1a7a38 !important; font-size: 28px; font-weight: 700; }
.result-diabetic p  { color: #7a0010 !important; }
.result-healthy  p  { color: #1a5c30 !important; }

.risk-high {
    background: rgba(230,57,70,0.1);
    border-left: 4px solid #e63946;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #ff6b6b !important;
    font-weight: 500;
}
.risk-ok {
    background: rgba(45,198,83,0.1);
    border-left: 4px solid #2dc653;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #2dc653 !important;
    font-weight: 500;
}

section[data-testid="stSidebar"] {
    background: #0d1b2a !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * { color: white !important; }

.stButton > button {
    background: linear-gradient(135deg, #0a9396, #005f73) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 32px !important;
    font-family: Poppins, sans-serif !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    width: 100% !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(10,147,150,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ═══════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════
if not st.session_state.logged_in:

    st.markdown("""
    <div style='text-align:center; padding:40px 0 20px;'>
        <div style='font-size:56px;'>🩺</div>
        <h1 style='color:white !important; font-size:32px; font-weight:700; margin:10px 0 4px;'>DiabetesAI</h1>
        <p style='color:rgba(255,255,255,0.6) !important; font-size:14px;'>Smart Diabetes Prediction System</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white !important; text-align:center; margin-bottom:6px;'>Welcome Back 👋</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:rgba(255,255,255,0.6) !important; text-align:center; font-size:13px; margin-bottom:24px;'>Login to access the system</p>", unsafe_allow_html=True)

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
        <div style='background:rgba(10,147,150,0.1); border:1px solid rgba(10,147,150,0.3); border-radius:10px; padding:12px; text-align:center;'>
            <p style='color:rgba(255,255,255,0.7) !important; font-size:12px; margin:0;'>
            🔑 Username: <b style='color:#94d2bd;'>admin</b> &nbsp;|&nbsp;
            Password: <b style='color:#94d2bd;'>diabetes13</b>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════
else:

    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <span style='font-size:32px;'>🩺</span>
        <h2 style='color:white !important; font-family:Poppins; font-weight:700; margin:4px 0;'>DiabetesAI</h2>
        <p style='color:rgba(255,255,255,0.5) !important; font-size:12px;'>Smart Diabetes Prediction System</p>
    </div>
    """, unsafe_allow_html=True)

    pages = [("🏠", "Home"), ("🔬", "Prediction"), ("⚠️", "Risk Factors"), ("🏥", "Health Recommendations")]
    cols  = st.columns(len(pages) + 1)

    for i, (icon, label) in enumerate(pages):
        with cols[i]:
            full     = f"{icon} {label}"
            selected = st.session_state.page == full
            style    = "background:rgba(10,147,150,0.25); border:1.5px solid #0a9396; box-shadow:0 4px 16px rgba(10,147,150,0.3);" if selected else "background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12);"
            st.markdown(f"""
            <div style='{style} border-radius:16px; padding:14px; text-align:center; margin-bottom:4px;'>
                <div style='font-size:26px;'>{icon}</div>
                <div style='font-size:10px; color:rgba(255,255,255,0.85); font-weight:500; text-transform:uppercase; letter-spacing:1px; margin-top:4px;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{label}", key=f"nav_{label}", use_container_width=True):
                st.session_state.page = full
                st.rerun()

    with cols[4]:
        st.markdown("""
        <div style='background:rgba(230,57,70,0.1); border:1px solid rgba(230,57,70,0.3); border-radius:16px; padding:14px; text-align:center; margin-bottom:4px;'>
            <div style='font-size:26px;'>🚪</div>
            <div style='font-size:10px; color:rgba(230,57,70,0.9); font-weight:500; text-transform:uppercase; letter-spacing:1px; margin-top:4px;'>Logout</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page = "🏠 Home"
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08); margin:8px 0 24px;'>", unsafe_allow_html=True)

    page = st.session_state.page

    # ═══════════════════════════════════════════════════
    # PAGE 1: HOME
    # ═══════════════════════════════════════════════════
    if page == "🏠 Home":
        st.markdown("""
        <div class='header-box'>
            <h1>🏠 Welcome to DiabetesAI</h1>
            <p>AI-powered diabetes risk assessment using Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:rgba(10,147,150,0.12); border:1.5px solid rgba(10,147,150,0.4); border-radius:16px; padding:32px 36px; margin-bottom:24px;'>
            <h3 style='color:#94d2bd !important; font-size:20px; margin-bottom:16px;'>🩺 About This App</h3>
            <p style='color:rgba(255,255,255,0.85) !important; font-size:15px; line-height:2;'>
            This application is designed to <b style='color:#94d2bd;'>predict whether a person is Diabetic or Not Diabetic</b>
            based on their medical details. By entering simple health parameters like
            Glucose level, BMI, Age, Blood Pressure, and Insulin,
            the system uses a trained <b style='color:#94d2bd;'>Random Forest Machine Learning Model</b>
            to instantly analyze the data and provide an accurate prediction result.
            The app also shows the <b style='color:#94d2bd;'>risk level</b> of each parameter and gives
            <b style='color:#94d2bd;'>personalized health recommendations</b> based on the result.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class='home-card'>
                <span class='icon'>🔬</span>
                <h4>Prediction</h4>
                <p>Enter 8 patient medical details and get instant prediction whether the patient is Diabetic or Not Diabetic with probability percentage.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='home-card'>
                <span class='icon'>⚠️</span>
                <h4>Risk Factor Analysis</h4>
                <p>After prediction, view detailed risk analysis of each medical parameter showing which values are Normal or High Risk.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class='home-card'>
                <span class='icon'>🏥</span>
                <h4>Health Recommendations</h4>
                <p>Get personalized health tips including diet recommendations, exercise tips, medical advice and lifestyle changes based on your result.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style='background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:14px; padding:24px; margin-top:8px;'>
            <h4 style='color:#94d2bd !important; margin-bottom:16px;'>🚀 How to Use This App?</h4>
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:12px;'>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0;'>1</span>
                    <p style='color:rgba(255,255,255,0.8) !important; margin:0; font-size:14px;'>Click <b style='color:#94d2bd;'>🔬 Prediction</b> icon above</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0;'>2</span>
                    <p style='color:rgba(255,255,255,0.8) !important; margin:0; font-size:14px;'>Enter patient medical details</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0;'>3</span>
                    <p style='color:rgba(255,255,255,0.8) !important; margin:0; font-size:14px;'>Click <b style='color:#94d2bd;'>⚡ Predict Now</b> button</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0;'>4</span>
                    <p style='color:rgba(255,255,255,0.8) !important; margin:0; font-size:14px;'>View Diabetic / Not Diabetic result</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0;'>5</span>
                    <p style='color:rgba(255,255,255,0.8) !important; margin:0; font-size:14px;'>Check <b style='color:#94d2bd;'>⚠️ Risk Factors</b> analysis</p>
                </div>
                <div style='display:flex; align-items:center; gap:12px;'>
                    <span style='background:#0a9396; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; flex-shrink:0;'>6</span>
                    <p style='color:rgba(255,255,255,0.8) !important; margin:0; font-size:14px;'>Get tips from <b style='color:#94d2bd;'>🏥 Health Consult</b></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════
    # PAGE 2: PREDICTION
    # ═══════════════════════════════════════════════════
    elif page == "🔬 Prediction":
        st.markdown("""
        <div class='header-box'>
            <h1>🔬 Diabetes Prediction</h1>
            <p>Enter patient medical details below</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='input-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#94d2bd !important; font-size:16px; font-weight:600; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px; margin-bottom:16px;'>👤 Patient Details</h4>", unsafe_allow_html=True)
            
            glucose     = st.number_input("Glucose (mg/dL)",       min_value=0,   max_value=300,  value=100, step=1)
            bp          = st.number_input("Blood Pressure (mmHg)", min_value=0,   max_value=200,  value=70,  step=1)
            skin        = st.number_input("Skin Thickness (mm)",   min_value=0,   max_value=100,  value=20,  step=1)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='input-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#94d2bd !important; font-size:16px; font-weight:600; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px; margin-bottom:16px;'>🏥 Medical Parameters</h4>", unsafe_allow_html=True)
            insulin = st.number_input("Insulin (μU/mL)",            min_value=0,   max_value=900,  value=80,  step=1)
            bmi     = st.number_input("BMI (kg/m²)",                min_value=0.0, max_value=70.0, value=25.0,step=0.1)
            dpf     = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0,  value=0.5, step=0.001, format="%.3f")
            age     = st.number_input("Age (years)",                min_value=1,   max_value=120,  value=30,  step=1)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("⚡ PREDICT NOW"):
            features        = np.array([[glucose, bp, skin, insulin, bmi, dpf, age]])
            features_scaled = scaler.transform(features)
            prediction      = int(model.predict(features_scaled)[0])
            probability     = float(model.predict_proba(features_scaled)[0][1]) * 100

            st.session_state["last_prediction"]  = prediction
            st.session_state["last_probability"] = probability
            st.session_state["last_inputs"] = {
                "glucose": glucose,
                "bp": bp, "skin": skin, "insulin": insulin,
                "bmi": bmi, "dpf": dpf, "age": age
            }

            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                if prediction == 1:
                    st.markdown(f"""
                    <div class='result-diabetic'>
                        <div style='font-size:52px;'>⚠️</div>
                        <h2>DIABETIC</h2>
                        <p style='color:#c1121f !important; font-size:15px; margin:8px 0;'>High diabetes risk detected</p>
                        <p style='font-size:13px; color:#7a0010 !important;'>Probability: <b>{probability:.1f}%</b></p>
                        <div style='background:rgba(0,0,0,0.1); border-radius:100px; height:10px; margin:12px 0; overflow:hidden;'>
                            <div style='width:{probability}%; height:100%; background:linear-gradient(90deg,#e63946,#ff8fa3); border-radius:100px;'></div>
                        </div>
                        <p style='font-size:12px; color:#c1121f !important;'>⚠️ Please consult a doctor immediately</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    healthy_prob = 100 - probability
                    st.markdown(f"""
                    <div class='result-healthy'>
                        <div style='font-size:52px;'>✅</div>
                        <h2>NOT DIABETIC</h2>
                        <p style='color:#1a7a38 !important; font-size:15px; margin:8px 0;'>Low diabetes risk detected</p>
                        <p style='font-size:13px; color:#1a5c30 !important;'>Healthy Probability: <b>{healthy_prob:.1f}%</b></p>
                        <div style='background:rgba(0,0,0,0.1); border-radius:100px; height:10px; margin:12px 0; overflow:hidden;'>
                            <div style='width:{healthy_prob}%; height:100%; background:linear-gradient(90deg,#2dc653,#69f0ae); border-radius:100px;'></div>
                        </div>
                        <p style='font-size:12px; color:#1a7a38 !important;'>✅ Maintain your healthy lifestyle!</p>
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='input-card'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color:#94d2bd !important;'>⚠️ Quick Risk Check</h4>", unsafe_allow_html=True)
                risks = [
                    ("🩸 Glucose",        glucose,  70,   140,  "mg/dL"),
                    ("⚖️ BMI",            bmi,      18.5, 24.9, "kg/m²"),
                    ("🎂 Age",            age,      0,    45,   "yrs"),
                    ("💉 Insulin",        insulin,  16,   166,  "μU/mL"),
                    ("🫀 Blood Pressure", bp,       60,   90,   "mmHg"),
                ]
                for name, val, low, high, unit in risks:
                    if val < low or val > high:
                        st.markdown(f"<div class='risk-high'>⚠️ {name}: {val} {unit} — Abnormal</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='risk-ok'>✅ {name}: {val} {unit} — Normal</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════
    # PAGE 3: RISK FACTORS
    # ═══════════════════════════════════════════════════
    elif page == "⚠️ Risk Factors":
        st.markdown("""
        <div class='header-box'>
            <h1>⚠️ Risk Factor Analysis</h1>
            <p>Detailed analysis of each medical parameter</p>
        </div>
        """, unsafe_allow_html=True)

        inputs = st.session_state.get("last_inputs", None)
        if inputs is None:
            st.warning("⚠️ Please run a prediction first from the 🔬 Prediction page!")
        else:
            risk_factors = [
                ("🩸 Glucose",           inputs["glucose"],     70,   140,  "mg/dL", "Primary indicator. High glucose means cells are not absorbing sugar properly."),
                ("⚖️ BMI",               inputs["bmi"],         18.5, 24.9, "kg/m²", "Higher BMI increases insulin resistance and diabetes risk."),
                ("🎂 Age",               inputs["age"],         0,    45,   "years",  "People above 45 are at higher risk of Type 2 diabetes."),
                ("💉 Insulin",           inputs["insulin"],     16,   166,  "μU/mL", "Abnormal insulin levels indicate pancreatic dysfunction."),
                ("🫀 Blood Pressure",    inputs["bp"],          60,   90,   "mmHg",  "High BP is associated with diabetes and heart issues."),
                ("🤰 Pregnancies",       inputs["pregnancies"], 0,    6,    "count",  "Higher pregnancies increase gestational diabetes risk."),
                ("🧬 Diabetes Pedigree", inputs["dpf"],         0,    0.8,  "score",  "Higher score means stronger family history of diabetes."),
                ("📏 Skin Thickness",    inputs["skin"],        10,   40,   "mm",    "Related to body fat and insulin resistance."),
            ]
            col1, col2 = st.columns(2)
            for i, (name, val, low, high, unit, desc) in enumerate(risk_factors):
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
                            <b style='color:white; font-size:15px;'>{name}</b>
                            <span style='color:{color}; font-size:12px; font-weight:600;'>{status}</span>
                        </div>
                        <div style='font-size:22px; font-weight:700; color:{color}; margin-bottom:6px;'>{val} <span style='font-size:13px; font-weight:400; color:rgba(255,255,255,0.6);'>{unit}</span></div>
                        <div style='font-size:11px; color:rgba(255,255,255,0.6); margin-bottom:8px;'>Normal: {low} – {high} {unit}</div>
                        <div style='font-size:12px; color:rgba(255,255,255,0.75); line-height:1.5;'>{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════
    # PAGE 4: HEALTH RECOMMENDATIONS
    # ═══════════════════════════════════════════════════
    elif page == "🏥 Health Recommendations":
        st.markdown("""
        <div class='header-box'>
            <h1>🏥 Health Recommendations</h1>
            <p>Personalized health recommendations</p>
        </div>
        """, unsafe_allow_html=True)

        prediction = st.session_state.get("last_prediction", None)
        if prediction is None:
            st.warning("⚠️ Please run a prediction first from the 🔬 Prediction page!")
        else:
            if prediction == 1:
                st.markdown("""
                <div style='background:rgba(230,57,70,0.1); border:1px solid #e63946; border-radius:14px; padding:20px; margin-bottom:24px;'>
                    <h3 style='color:#e63946 !important; margin-bottom:6px;'>⚠️ High Risk — Please Follow These Steps</h3>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0;'>Your result indicates high diabetes risk. Follow these recommendations carefully.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='background:rgba(45,198,83,0.1); border:1px solid #2dc653; border-radius:14px; padding:20px; margin-bottom:24px;'>
                    <h3 style='color:#2dc653 !important; margin-bottom:6px;'>✅ Low Risk — Keep Maintaining Your Health</h3>
                    <p style='color:rgba(255,255,255,0.85) !important; margin:0;'>Your result shows low risk. Follow these tips to stay healthy.</p>
                </div>
                """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <div class='input-card'>
                    <h4 style='color:#94d2bd !important; margin-bottom:14px;'>🥗 Diet Recommendations</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2; padding-left:18px;'>
                        <li>Avoid sugary drinks and sweets</li>
                        <li>Eat more vegetables and fruits</li>
                        <li>Choose whole grains over refined grains</li>
                        <li>Limit white rice and white bread</li>
                        <li>Drink 8-10 glasses of water daily</li>
                        <li>Eat small meals every 3-4 hours</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class='input-card' style='margin-top:14px;'>
                    <h4 style='color:#94d2bd !important; margin-bottom:14px;'>🏃 Exercise Tips</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2; padding-left:18px;'>
                        <li>Walk at least 30 minutes daily</li>
                        <li>Do light exercises 5 days a week</li>
                        <li>Try yoga or swimming</li>
                        <li>Avoid sitting for long hours</li>
                        <li>Maintain a healthy body weight</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div class='input-card'>
                    <h4 style='color:#94d2bd !important; margin-bottom:14px;'>🏥 Medical Advice</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2; padding-left:18px;'>
                        <li>Consult a doctor if high risk</li>
                        <li>Check blood sugar levels regularly</li>
                        <li>Monitor blood pressure weekly</li>
                        <li>Get HbA1c test every 3 months</li>
                        <li>Take prescribed medicines on time</li>
                        <li>Do not skip doctor appointments</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                <div class='input-card' style='margin-top:14px;'>
                    <h4 style='color:#94d2bd !important; margin-bottom:14px;'>😴 Lifestyle Changes</h4>
                    <ul style='color:rgba(255,255,255,0.85) !important; line-height:2; padding-left:18px;'>
                        <li>Sleep 7-8 hours every night</li>
                        <li>Avoid smoking and alcohol</li>
                        <li>Manage stress with meditation</li>
                        <li>Keep track of daily food intake</li>
                        <li>Stay hydrated throughout the day</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
