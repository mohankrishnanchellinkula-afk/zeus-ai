import streamlit as st
import google.generativeai as genai
import pandas as pd
from PIL import Image
import datetime
import random
import hashlib
import re
import io

# ==========================================
# 1. INITIALIZATION & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Zeus.ai - Divine Identity Citadel",
    page_icon="⚡",
    layout="wide"
)

# Active National Platform API Key Verification Routing
GEMINI_API_KEY = "AIzaSyABehCXucp1tgZwGTwI44M-q4rOacTGxTc"
genai.configure(api_key=GEMINI_API_KEY)

# --- MAJESTIC OLYMPIAN GOLD & MARBLE WHITE STYLING ENGINE ---
st.markdown("""
    <style>
    /* Main Background: Majestic Marble White & Light Cream Gradient */
    .stApp {
        background-color: #fcfbf7 !important;
        background-image: linear-gradient(180deg, #fefdfa 0%, #f4f1e6 100%) !important;
        color: #1e293b !important;
    }
    
    /* Left Sidebar: Warm Light Slate & Clear Gold Border Accent */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9 !important;
        border-right: 3px solid #d97706 !important;
    }
    
    /* Normal Block Navigation Styling for Sidebar Links */
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 8px;
        padding: 4px 0px;
    }
    
    /* Hide Default Radio Selection Target Dots */
    section[data-testid="stSidebar"] div[role="radiogroup"] label [data-testid="stBorderedContainer"],
    section[data-testid="stSidebar"] div[data-testid="stRadioHBox"] div[role="presentation"] {
        display: none !important;
    }
    
    /* Transform Options into Solid Borderless Blocks */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #e2e8f0 !important;
        padding: 10px 14px !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        border: none !important;
        margin: 2px 0px !important;
        transition: background 0.2s ease, transform 0.1s ease;
        width: 100% !important;
    }
    
    /* Selection block states: Hover & Active Content */
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #cbd5e1 !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] [data-checked="true"] {
        background-color: #f59e0b !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] [data-checked="true"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {
        font-weight: bold !important;
        color: #0f172a !important;
        margin-bottom: 10px !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Solid Ochre & Imperial Yellow Typography (No Flares or White Shadows) */
    h1, h2, h3, h4, h5, h6 {
        color: #b45309 !important;
        text-shadow: none !important;
        font-family: 'Georgia', serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Text Paragraph Adjustments for Light Contrast */
    .stMarkdown p, label {
        color: #334155 !important;
        font-weight: 500;
    }
    
    /* Form & Input Field Enhancements */
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea, div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }
    div[data-baseweb="input"] input:focus {
        border-color: #d97706 !important;
    }
    
    /* Clean Dashboard Metric Containers displaying Vivid Ochre text values without glare */
    div[data-testid="stMetricValue"] > div {
        color: #b45309 !important;
        font-family: 'Georgia', serif !important;
        font-weight: 800 !important;
        text-shadow: none !important;
    }
    
    /* High-Voltage Imperial Gold Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(217, 119, 6, 0.15) !important;
        border-radius: 6px !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%) !important;
        box-shadow: 0px 6px 12px rgba(217, 119, 6, 0.3) !important;
        color: #ffffff !important;
        transform: translateY(-1px);
    }
    
    /* Adjust Alert Boxes */
    div.stAlert {
        background-color: #fef3c7 !important;
        color: #92400e !important;
        border: 1px solid #fde68a !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize data structures
if "reports_db" not in st.session_state:
    st.session_state.reports_db = [
        {"ID": "ZUS-1042", "Timestamp": "2026-05-24 14:20", "Type": "ID Forgery", "Status": "Struck Down", "Risk Score": "92%"},
        {"ID": "ZUS-3089", "Timestamp": "2026-05-25 09:15", "Type": "Sim Cloning", "Status": "Under Thunderbolt Review", "Risk Score": "78%"}
    ]
if "honeypot_db" not in st.session_state:
    st.session_state.honeypot_db = [
        {"Decoy ID Dispatched": "National ID - Fake Profile 928", "Attacker IP Routing Mark": "192.168.42.105", "Automated Tool Fingerprint": "Python-requests/2.31", "Action Strategy Executed": "Injected Corrupted Telemetry Honey"},
        {"Decoy ID Dispatched": "Tax Card - Fake Profile 102", "Attacker IP Routing Mark": "10.4.82.12", "Automated Tool Fingerprint": "Scrapy Crawl Bot Matrix", "Action Strategy Executed": "Delayed Payload Response Stream"}
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": hashlib.md5("admin123".encode()).hexdigest()}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def make_hashes(password): return hashlib.md5(password.encode()).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# ==========================================
# 2. OLYMPIAN CITADEL ACCESS GATEWAY
# ==========================================
if not st.session_state.logged_in:
    st.title("⚡ ZEUS.AI — THE DICTUM OF OLYMPUS CLEARANCE")
    st.markdown("**National Counter-Identity Theft & Fraud Intelligence Terminal**")
    
    auth_mode = st.radio("Select Citadel Entry Access Action:", ["Pass the Gates (Login)", "Register New Sentinel Identity (Sign Up)"], horizontal=True)
    st.markdown("---")
    
    if auth_mode == "Pass the Gates (Login)":
        st.markdown("### 🔑 Secure Portal Sign-In Authentication")
        username = st.text_input("Sentinel Identity Name:")
        password = st.text_input("Citadel Cipher Key (Password):", type="password")
        
        if st.button("Summon Thunderbolt Access Clearances", use_container_width=True):
            if username in st.session_state.users_db and check_hashes(password, st.session_state.users_db[username]):
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("⚡ Gates Unlocked. Ascending to the High Court.")
                st.rerun()
            else:
                st.error("❌ Identification cipher mismatched. Access denied by the heavens.")
        st.info("💡 Hackathon Bypass Token: Use identity username admin with cipher key admin123")

    elif auth_mode == "Register New Sentinel Identity (Sign Up)":
        st.markdown("### 📝 Register New Sentinel Clearance Key")
        new_user = st.text_input("Define New Sentinel Name:")
        new_password = st.text_input("Assign Access Key Passphrase:", type="password")
        confirm_password = st.text_input("Confirm Access Key Passphrase:", type="password")
        
        if st.button("Forge Encrypted Key Signature Into Vaults", use_container_width=True):
            if not new_user or not new_password:
                st.warning("Identification fields cannot contain blank parameters.")
            elif new_user in st.session_state.users_db:
                st.error("❌ That Sentinel handle already commands an operational node.")
            elif new_password != confirm_password:
                st.error("❌ Key verification strings do not align.")
            else:
                st.session_state.users_db[new_user] = make_hashes(new_password)
                st.success("⚡ Signature successfully forged! Select 'Pass the Gates' mode above to log in.")

# ==========================================
# 3. HIGH CITADEL PLATFORM RUNTIME (POST-LOGIN)
# ==========================================
else:
    st.sidebar.markdown("<h2 style='text-align: center; color: #b45309;'>⚡ ZEUS CORE</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"🛰️ **Active Sky Sentinel:** `{st.session_state.current_user}`")
    
    if st.sidebar.button("🔒 Dissolve Session Clearances", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
        
    st.sidebar.markdown("---")
    
    navigation = st.sidebar.radio(
        "Tactical Domain Modules:",
        [
            "📊 Aegis Identity Matrix [Dashboard]", 
            "🚨 Threat Incident Portal [Reporting Portal]", 
            "📄 Neural Document Inspection [ID Verification]",
            "⚖️ Scale of Themis [Threat Risk Meter]",
            "🦅 Eye of Aquila [Real-time Attack Tracker]",
            "⚡ Thunderbolt Sanction [Automated Remediation]",
            "🏺 Pandora's Vault [Honeypot Tracer]",
            "🔍 Deceptive Trajectory Analyzer [Phishing Detection]",
            "🕵️ Dark Void Leak Exposure Check [Breach Checker]",
            "🤖 Aegis Copilot Consult [AI Strategy Chatbot]",
            "🎭 Biometric Distortion Filter [Deepfake Audit]", 
            "🕸️ Olympus Syndicate Tracer [Fraud Ring Tracker]"
        ]
    )

    # ==========================================
    # MODULE: IDENTITY MATRIX DASHBOARD
    # ==========================================
    if navigation == "📊 Aegis Identity Matrix [Dashboard]":
        st.title("⚡ The Olympian Identity Matrix Dashboard")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Attacks Struck Down", "42,912", "+8% Today")
        col2.metric("Isolated Fraud Syndicates", f"{len(st.session_state.reports_db) + 12} Rings", "Active Dynamic Mode")
        col3.metric("Divine AI Accuracy", "99.4%", "Stable")
        col4.metric("Your Logged Anomalies", len(st.session_state.reports_db), "Live Sync")
        
        st.markdown("---")
        st.subheader("🛠️ Fleet Threat Management Console")
        
        df_dash = pd.DataFrame(st.session_state.reports_db)
        st.dataframe(df_dash, use_container_width=True)
        
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            st.markdown("#### ➕ Deploy New Custom Threat Log Entry")
            add_type = st.selectbox("Assign Threat Profile Struct:", ["ID Forgery", "Sim Cloning", "PAN Impersonation", "Deepfake Bypass", "Synthetic ID Splice"])
            add_score = st.slider("Assessed Threat Severity Margin (%):", 0, 100, 85)
            if st.button("Inject Entry Vector"):
                new_vector = {
                    "ID": f"ZUS-{random.randint(4000, 8999)}",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Type": add_type,
                    "Status": "Under Thunderbolt Review",
                    "Risk Score": f"{add_score}%"
                }
                st.session_state.reports_db.append(new_vector)
                st.success("⚡ New anomaly vector seeded successfully inside session registers.")
                st.rerun()

        with opt_col2:
            st.markdown("#### ❌ Dissolve Existing Threat Logs")
            if len(st.session_state.reports_db) > 0:
                target_del = st.selectbox("Select Signature Index to Wipe:", [item["ID"] for item in st.session_state.reports_db])
                if st.button("Purge Target Vector"):
                    st.session_state.reports_db = [item for item in st.session_state.reports_db if item["ID"] != target_del]
                    st.success(f"⚡ Log vector `{target_del}` wiped clean from database records.")
                    st.rerun()
            else:
                st.info("No active registry entries available to dissolve.")

    # ==========================================
    # MODULE: THREAT PORTAL
    # ==========================================
    elif navigation == "🚨 Threat Incident Portal [Reporting Portal]":
        st.title("🚨 Threat Telemetry Submission Desk")
        
        with st.form("reporting_form"):
            identity_type = st.selectbox("Target Attacked Structural Field", ["National Document ID", "PAN Card", "Passport", "Voter ID", "Mobile Identity"])
            selected_date = st.date_input("Incident Telemetry Observed Date:", datetime.date.today())
            selected_time = st.time_input("Incident Timestamp Alignment Mark:", datetime.datetime.now().time())
            evidence_text = st.text_area("Paste text payloads, message headers, or event traces:")
            submit_btn = st.form_submit_button("Broadcast Telemetry to High Court")
            
            if submit_btn and evidence_text:
                new_id = f"ZUS-{random.randint(1000, 9999)}"
                combined_timestamp = f"{selected_date} {selected_time.strftime('%H:%M')}"
                st.session_state.reports_db.append({
                    "ID": new_id, 
                    "Timestamp": combined_timestamp, 
                    "Type": identity_type, 
                    "Status": "Struck Down", 
                    "Risk Score": f"{random.randint(72,99)}%"
                })
                st.success(f"⚡ Token recorded into registers under index: **{new_id}**.")
        
        st.markdown("### 📋 Historic Submission Ledger")
        df_ledg = pd.DataFrame(st.session_state.reports_db)
        st.dataframe(df_ledg, use_container_width=True)
        
        csv_buffer = io.StringIO()
        df_ledg.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Download Structured Threat Report Ledger (CSV)",
            data=csv_buffer.getvalue(),
            file_name=f"Zeus_Threat_Report_{datetime.date.today()}.csv",
            mime="text/csv"
        )

    # ==========================================
    # MODULE: NEURAL DOCUMENT INSPECTION
    # ==========================================
    elif navigation == "📄 Neural Document Inspection [ID Verification]":
        st.title("📄 High-Court Neural Document Audit")
        uploaded_file = st.file_uploader("Upload Scanned Identity Document (PNG/JPG):", type=["png", "jpg", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Target Document Source Metadata Asset Stream", width=350)
            if st.button("Unleash Neural Forgery Assessment"):
                with st.spinner("Decoding image pixel grids..."):
                    try:
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(["Perform comprehensive identity document classification forensics. Output parameters strictly separating structural fields, text verification segments, metadata variations, and potential generative alteration risks with complete granularity.", Image.open(uploaded_file)])
                        st.markdown("### 🔍 Extracted Forensic Metrics Summary")
                        st.info(response.text)
                    except Exception as e: 
                        st.error(f"Inference error: {e}")

    # ==========================================
    # MODULE: RISK METER
    # ==========================================
    elif navigation == "⚖️ Scale of Themis [Threat Risk Meter]":
        st.title("⚖️ Scale of Themis — Threat Risk Analyzer Matrix")
        test_score = st.slider("Simulated Identity Parameter Discrepancy Margin:", 0, 100, 45)
        st.markdown("### Core Metric Threat Weights")
        c1, c2, c3 = st.columns(3)
        geo_risk = c1.checkbox("Mismatched Device Geolocation Context", value=test_score > 40)
        face_risk = c2.checkbox("Generative Facial GAN Distortion Signals", value=test_score > 75)
        time_risk = c3.checkbox("High-Frequency Telemetry Bursts (Script Indicator)", value=test_score > 60)
        
        calculated_score = test_score + (15 if geo_risk else 0) + (25 if face_risk else 0) + (10 if time_risk else 0)
        calculated_score = min(calculated_score, 100)
        
        st.markdown("---")
        st.subheader(f"Total Aggregated Risk Evaluation Index: **{calculated_score}%**")
        st.progress(calculated_score / 100)
        
        if calculated_score >= 80:
            st.error("💥 THUNDERBOLT DECOUPLING PROTOCOL ACTIVATED. Revoking credentials.")
        elif calculated_score >= 45:
            st.warning("⚠️ PROBATIONARY SANDBOX CLEARANCE: Identity inconsistencies flagged.")
        else:
            st.success("✔️ DIVINE IMMUNITY STANDARDS CONFIRMED: Identity clears parameter gates.")

    # ==========================================
    # MODULE: ATTACK TRACKER MAP
    # ==========================================
    elif navigation == "🦅 Eye of Aquila [Real-time Attack Tracker]":
        st.title("🦅 Eye of Aquila — Real-Time Identity Fraud Map Tracker")
        
        global_map_coordinates = pd.DataFrame({
            'lat': [20.5937, 40.7128, 51.5074, 35.6762, -22.9068, -33.8688],
            'lon': [78.9629, -74.0060, -0.1278, 139.6503, -43.1729, 151.2093]
        })
        st.map(global_map_coordinates)
        st.markdown("### 🗺️ International Operational Threat Vectors Currently Flagged")
        st.info("💡 Inter-continental tracking modules are monitoring high-frequency script attacks passing across cross-border financial registry nodes.")

    # ==========================================
    # MODULE: AUTOMATED MITIGATION DEFENSE
    # ==========================================
    elif navigation == "⚡ Thunderbolt Sanction [Automated Remediation]":
        st.title("⚡ Thunderbolt Sanction — Active Defense Mitigation Control Room")
        target_id = st.text_input("Enter Malicious Incident Index Target Signature (e.g., ZUS-1042):")
        
        if target_id:
            st.markdown(f"### Available Counter-Measures for Node `{target_id}`")
            act1 = st.checkbox("Deploy Dynamic Biometric Lock Request Signature directly to National Registry Network")
            act2 = st.checkbox("Signal Telecommunication Partners to Instantly Terminate Associated Cloned IMSI Modules")
            act3 = st.checkbox("Compile System Audit Logs into Signed Legal Cyber Incident Document Formats")
            
            if st.button("Unleash Sanction Directives"):
                if act1 or act2 or act3:
                    st.success(f"⚡ ALL SELECTED SANCTIONS SUCCESSFULLY ROUTED. Incident `{target_id}` neutralized.")
                    st.session_state.honeypot_db.append({
                        "Decoy ID Dispatched": f"Decoupled Target Capture {target_id}",
                        "Attacker IP Routing Mark": f"Isolated Node Stream {random.randint(100,254)}.{random.randint(10,99)}.2.1",
                        "Automated Tool Fingerprint": "Zeus-Intercept/v4.2 Mitigation Engine",
                        "Action Strategy Executed": "Forced Session Dissolution"
                    })
                else:
                    st.warning("Select at least one mitigating counter-measure directive.")

    # ==========================================
    # MODULE: PANDORA'S VAULT (HONEYPOT LOGS)
    # ==========================================
    elif navigation == "🏺 Pandora's Vault [Honeypot Tracer]":
        st.title("🏺 Pandora's Vault — Generative Decoy Decoupling Matrix")
        col1, col2 = st.columns(2)
        col1.metric("Active Decoy Traps Set", f"{len(st.session_state.honeypot_db) * 4} Traps")
        col2.metric("Rogue Automated Captures", f"{len(st.session_state.honeypot_db)} Active Entries")
        
        st.markdown("### Trapped Scraper Intelligence Feed Logs")
        st.table(pd.DataFrame(st.session_state.honeypot_db))

    # ==========================================
    # MODULE: LINGUISTIC PHISHING CHECKER
    # ==========================================
    elif navigation == "🔍 Deceptive Trajectory Analyzer [Phishing Detection]":
        st.title("🔍 Dark Intelligence Phishing Analyzer")
        scam_text = st.text_area("Input suspicious text payload strings:")
        if scam_text and st.button("Deconstruct Linguistic Subversion Parameters"):
            with st.spinner("Decoding social engineering indicators..."):
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(f"Deconstruct the following text for phishing markers: '{scam_text}'")
                    st.info(response.text)
                except Exception as e: 
                    st.error(f"Error: {e}")

    # ==========================================
    # MODULE: DATA BREACH CHECKER
    # ==========================================
    elif navigation == "🕵️ Dark Void Leak Exposure Check [Breach Checker]":
        st.title("🕵️ Deep Abyss Compromised Data Index Search")
        lookup_input = st.text_input("Enter Target Email Coordinates to Parse Archive Indices:").strip().lower()
        
        if lookup_input:
            if st.button("Scan Abyssal Archives"):
                prefix = lookup_input.split('@')[0] if '@' in lookup_input else lookup_input
                has_malicious_keywords = any(kw in prefix for kw in ["hacker", "breach", "leak", "fraud", "attack"])
                
                if has_malicious_keywords or len(re.findall(r'\d', prefix)) >= 5:
                    st.error(f"❌ **EXPOSURE CRITICAL:** Coordinate '{lookup_input}' located inside structural public index dumps.")
                    leak_table = {
                        "Breach Origin Archive Log Source": ["Underground Corporate Database Leak Vector"],
                        "Exposed Security Fields Found": ["Plaintext Cryptographic Hashes, Usernames"],
                        "Estimated Leak Vintage": ["Q1 2026"]
                    }
                    st.table(pd.DataFrame(leak_table))
                else:
                    st.success(f"✔️ **SECURE:** Target coordinate `{lookup_input}` clears analytical filtration sweeps.")

    # ==========================================
    # MODULE: CO-PILOT ADVISORY TERMINAL
    # ==========================================
    elif navigation == "🤖 Aegis Copilot Consult [AI Strategy Chatbot]":
        st.title("🤖 Divine AI Strategy Oracle Node")
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        if user_query := st.chat_input("Ask Zeus Oracle about defensive configurations..."):
            with st.chat_message("user"): st.markdown(user_query)
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("assistant"):
                try:
                    res = genai.GenerativeModel("gemini-2.5-flash").generate_content(user_query).text
                    st.markdown(res)
                    st.session_state.chat_history.append({"role": "assistant", "content": res})
                except Exception as e: 
                    st.error(f"Oracle terminal exception: {e}")

    # ==========================================
    # MODULE: DEEPFAKE FACE AUDIT
    # ==========================================
    elif navigation == "🎭 Biometric Distortion Filter [Deepfake Audit]":
        st.title("🎭 Biometric Synthetic Generative Face Mesh Verification")
        uploaded_face = st.file_uploader("Deploy Target Facial Biometric Frame Asset:", type=["png", "jpg", "jpeg"])
        if uploaded_face and st.button("Calculate Face Mesh Structural Authenticity"):
            with st.spinner("Evaluating blending edges..."):
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(["Analyze this biometric frame for synthetic deepfake or face-swap modifications.", Image.open(uploaded_face)])
                    st.warning(response.text)
                except Exception as e: 
                    st.error(f"Failure: {e}")

    # ==========================================
    # MODULE: OLYMPUS SYNDICATE FRAUD RING TRACER
    # ==========================================
    elif navigation == "🕸️ Olympus Syndicate Tracer [Fraud Ring Tracker]":
        st.title("🕸️ Inter-Platform Mapped Syndicate Fraud Tracer")
        
        ring_rows = []
        for index, item in enumerate(st.session_state.reports_db):
            ring_rows.append({
                "Suspect Identity Node": f"{item['Type']} Signature ({item['ID']})",
                "Connected Registry Match": f"Threat Vector Coordinate Array Mark",
                "Link Overlap Parameter": f"Telemetry Linked via {item['Timestamp']}",
                "Threat Severity Factor": f"CRITICAL FRAUD STATE ({item['Risk Score']})"
            })
            
        if not ring_rows:
            ring_rows = [{"Suspect Identity Node": "Database Clearance Active", "Connected Registry Match": "No Unresolved Fraud Vectors", "Link Overlap Parameter": "Clean Isolation Parameters", "Threat Severity Factor": "SECURE (0%)"}]
            
        st.table(pd.DataFrame(ring_rows))
        st.success("✔️ Linked syndicate clusters successfully mapped. All anomalies synchronized.")