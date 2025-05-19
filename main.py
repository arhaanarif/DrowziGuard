import streamlit as st
import subprocess
import threading
import base64
import os

# Force Streamlit to use a light theme and expand sidebar
st.set_page_config(page_title="Drowsiness Detection Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Royal Green and White Theme with Tahoma Font
st.markdown(
    """
    <style>
        /* Import Tahoma font */
        @import url('https://fonts.googleapis.com/css2?family=Tahoma&display=swap');
        
        /* Force royal theme for all Streamlit containers */
        body, .stApp, .main, .block-container {
            background-color: #f0fff0 !important;
            color: #333333 !important;
            font-family: 'Tahoma', sans-serif !important;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #006400 !important;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
            font-family: 'Tahoma', sans-serif !important;
        }
        [data-testid="stSidebar"] a {
            color: #ffffff !important;
        }
        
        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #006400, #228b22);
            padding: 3rem;
            border-radius: 10px;
            text-align: center;
            color: #ffffff;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 2.5rem;
            font-weight: bold;
            animation: typing 3s steps(40, end), blink-caret 0.75s step-end infinite;
            overflow: hidden;
            border-right: 0.15em solid #ffffff;
            margin: 0 auto;
            font-family: 'Tahoma', sans-serif;
            line-height: 1.2;
        }
        .hero-tagline {
            font-size: 1.5rem;
            margin-top: 1rem;
            opacity: 0;
            animation: fadeIn 2s ease-in forwards;
            animation-delay: 3s;
        }
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        @keyframes blink-caret {
            from, to { border-color: transparent; }
            50% { border-color: #ffffff; }
        }
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        
        @media (max-width: 768px) {
            .hero-title {
                padding: 2rem;
            }
            .hero-tagline {
                font-size: 1.2rem;
            }
        }
        @media (max-width: 480px) {
            .hero-title {
                font-size: 1.8rem;
            }
            .hero-tagline {
                font-size: 1rem;
            }
        }

        .download-button {
            background-color: #ffffff !important;
            color: #006400 !important;
            padding: 0.8rem 2rem;
            border-radius: 8px;
            border: none;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
            font-family: 'Tahoma', sans-serif;
        }
        .download-button:hover {
            background-color: #e0e0e0 !important;
            transform: scale(1.05);
        }
        
        /* News Banner */
        .news-banner {
            width: 100%;
            overflow: hidden;
            background: linear-gradient(90deg, #e6f0fa, #f5f7fa);
            color: #006400;
            font-weight: bold;
            font-size: 1rem;
            padding: 0.8rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            marginたる: 2rem;
            font-family: 'Tahoma', sans-serif;
        }
        .scrolling-text {
            display: inline-block;
            white-space: nowrap;
            animation: scroll-left 20s linear infinite;
        }
        @keyframes scroll-left {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        /* Button Styling */
        .stButton>button[kind="primary"] {
            display: block;
            margin: 0 auto;
            padding: 0.8rem 2rem;
            font-size: 1.2rem;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: #006400 !important;
            color: #ffffff !important;
            width: 200px;
            text-align: center;
            font-family: 'Tahoma', sans-serif;
        }
        .stButton>button[kind="primary"]:hover {
            background-color: #004d00 !important;
            transform: scale(1.05);
        }
        .stButton>button:not([kind="primary"]) {
            display: block;
            margin: 0 auto;
            padding: 0.8rem 2rem;
            font-size: 1.2rem;
            font-weight: bold;
            border: 3px solid #dc3545;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: #ffffff !important;
            color: #dc3545 !important;
            width: 200px;
            text-align: center;
            font-family: 'Tahoma', sans-serif;
        }
        .stButton>button:not([kind="primary"]):hover {
            background-color: #f8f9fa !important;
            transform: scale(1.05);
        }
        
        /* Feedback Submit Button Styling */
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #ffffff !important;
            color: #dc3545 !important;
            border: 3px solid #dc3545 !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            font-family: 'Tahoma', sans-serif;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #f8f9fa !important;
            transform: scale(1.05) !important;
        }
        
        /* Card Styling */
        .feature-card, .info-card, .tech-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            transition: transform 0.3s;
        }
        .feature-card:hover, .info-card:hover, .tech-card:hover {
            transform: translateY(-5px);
        }
        .feature-card h4, .info-card h4, .tech-card h4 {
            color: #006400;
            margin-bottom: 0.5rem;
            font-family: 'Tahoma', sans-serif;
        }
        .feature-card p, .info-card p, .tech-card p {
            color: #333333;
            font-size: 0.95rem;
            font-family: 'Tahoma', sans-serif;
        }
        
        /* Feedback Form Styling */
        .feedback-form {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-top: 2rem;
        }
        .feedback-form h4 {
            color: #006400;
            margin-bottom: 1rem;
            font-family: 'Tahoma', sans-serif;
        }
        
        /* Filler Section */
        .filler-section {
            margin-top: 2rem;
            padding: 1rem;
            background-color: #e6f0fa;
            border-radius: 10px;
            text-align: center;
            font-family: 'Tahoma', sans-serif;
        }
        
        /* Footer Styling */
        .footer {
            text-align: center;
            color: #6c757d;
            margin-top: 3rem;
            padding: 1rem;
            font-family: 'Tahoma', sans-serif;
        }
        .footer a {
            color: #006400;
            text-decoration: none;
            margin: 0 0.5rem;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* Ensure main content text contrast */
        p, li, h1, h2, h3, h4 {
            color: #333333 !important;
            font-family: 'Tahoma', sans-serif !important;
        }
        
        /* Button container */
        .button-container {
            display: flex;
            justify-content: center;
            margin: 1rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with About Us Information
with st.sidebar:
    st.markdown("<h2>About This Project</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <div>
            <p>This Driver Drowsiness Detection System uses a deep learning model along with 
            real-time webcam input to monitor a driver's alertness. It detects drowsy 
            states using eye and mouth features, and also tracks eye closure using MediaPipe for 
            blink detection. If the eyes stay closed for more than 5 seconds or drowsiness is predicted 
            by the model, it triggers an alarm and displays a warning. The system helps in preventing 
            accidents caused by driver fatigue.</p>
            <h4>Problem Statement</h4>
            <p>Drowsiness and fatigue are major causes of road accidents, especially during long drives or night travel. 
            Drivers often fail to realize when they are too tired to drive safely. Traditional systems lack real-time 
            monitoring or are too expensive for widespread use. There is a need for an affordable, real-time solution 
            that can alert drivers before accidents occur due to drowsiness.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Scrolling News Banner
st.markdown(
    """
    <div class='news-banner'>
        <div class='scrolling-text'>🚨 Drowsy driving causes 20% of road accidents. Stay alert, stay safe! 🚨</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Hero Section with Animated Title and Download Button
st.markdown(
    """
    <div class='hero-section'>
        <div class='hero-title'>DrowziGuard - AI Powered Driver Drowsiness Detection System</div>
        <div class='hero-tagline'>Stay Alert, Drive Safe with AI-Powered Monitoring</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Project Report Download Button
# Placeholder PDF content (in a real scenario, you'd upload a real PDF)
pdf_file_path = os.path.join("Assets","DrowziGuard_Report.pdf")
if os.path.exists(pdf_file_path):
    with open(pdf_file_path, "rb") as f:
        pdf_content = f.read()
else:
    st.error("PDF file not found at assets/DrowziGuard_Report.pdf")
    pdf_content = b""

# pdf_content = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Project Report Placeholder) Tj\nET\nendstream\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
st.download_button(
    label="📥 Download Project Report",
    data=pdf_content,
    file_name="Drowziguard.pdf",
    mime="application/pdf",
    key="download_report",
    use_container_width=False,
    type="primary"
)
# Center the download button
st.markdown(
    """
    <style>
        div[data-testid="stDownloadButton"] {
            display: flex;
            justify-content: center;
        }
        div[data-testid="stDownloadButton"] > button {
            background-color: #ffffff !important;
            color: #006400 !important;
            padding: 0.8rem 2rem !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: bold !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            font-family: 'Tahoma', sans-serif !important;
        }
        div[data-testid="stDownloadButton"] > button:hover {
            background-color: #e0e0e0 !important;
            transform: scale(1.05) !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered Start/Stop Buttons and Credit
if "detection_process" not in st.session_state:
    st.session_state.detection_process = None
    st.session_state.detection_running = False

def start_detection():
    if not st.session_state.detection_running:
        st.session_state.detection_running = True
        st.session_state.detection_process = subprocess.Popen(["python", "detection.py"])
        st.success("✅ Detection started. Check the OpenCV window.")

def stop_detection():
    if st.session_state.detection_running and st.session_state.detection_process:
        st.session_state.detection_process.terminate()
        st.session_state.detection_process = None
        st.session_state.detection_running = False
        st.success("🛑 Detection stopped.")

# Button container
st.markdown("<div class='button-container'>", unsafe_allow_html=True)
if not st.session_state.detection_running:
    st.button("▶️ Start Detection", key="start", on_click=start_detection, 
              help="Start the drowsiness detection system", type="primary")
else:
    st.button("🛑 Stop Detection", key="stop", on_click=stop_detection, 
              help="Stop the drowsiness detection system", type="secondary")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #6c757d; font-family: Tahoma, sans-serif;'>Dissertation Project | Built by Arhaan Arif | Enrollment No: 2021-310-043</p>", unsafe_allow_html=True)

# Status Indicator
if st.session_state.detection_running:
    st.markdown("<p style='text-align: center; color: #006400; font-weight: bold; font-family: Tahoma, sans-serif;'>Detection Running...</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align: center; color: #6c757d; font-family: Tahoma, sans-serif;'>Detection Stopped</p>", unsafe_allow_html=True)

# Key Features Section
st.markdown("<h2 style='text-align: center; color: #006400; font-family: Tahoma, sans-serif;'>Key Features</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class='feature-card'>
            <h4>🚨 Real-Time Alerts</h4>
            <p>Instant audio and visual warnings when drowsiness or prolonged eye closure is detected.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <div class='feature-card'>
            <h4>👁️ Eye & Blink Monitoring</h4>
            <p>Tracks eye aspect ratio using facial landmarks for precise blink detection.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <div class='feature-card'>
            <h4>🧠 AI-Powered Detection</h4>
            <p>Employs deep learning models to identify drowsiness patterns in real-time.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Technologies Used Section
st.markdown("<h2 style='text-align: center; color: #006400; font-family: T meekness, sans-serif;'>Technologies Used</h2>", unsafe_allow_html=True)
col_tech1, col_tech2, col_tech3 = st.columns(3)
with col_tech1:
    st.markdown(
        """
        <div class='tech-card'>
            <h4>🐍 Python</h4>
            <p>The core programming language used for building the system, enabling rapid development and integration of AI models.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_tech2:
    st.markdown(
        """
        <div class='tech-card'>
            <h4>🧠 Deep Learning</h4>
            <p>Utilizes neural networks to analyze facial features and detect drowsiness patterns in real-time.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_tech3:
    st.markdown(
        """
        <div class='tech-card'>
            <h4>🔬 TensorFlow</h4>
            <p>An open-source framework for training and deploying the MobileNetV2 model for drowsiness detection.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

col_tech4, col_tech5, _ = st.columns(3)
with col_tech4:
    st.markdown(
        """
        <div class='tech-card'>
            <h4>📊 Streamlit</h4>
            <p>An open-source Python library used to create this interactive web dashboard for controlling and monitoring the system.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_tech5:
    st.markdown(
        """
        <div class='tech-card'>
            <h4>📍 MediaPipe</h4>
            <p>Google's framework for facial landmark detection, enabling precise tracking of eye and mouth features.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Information Sections
st.markdown("<h2 style='text-align: center; color: #006400; font-family: Tahoma, sans-serif;'>Drowsiness & Safety Information</h2>", unsafe_allow_html=True)
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.markdown(
        """
        <div class='info-card'>
            <h4>🛑 Did You Know?</h4>
            <ul>
                <li>Driver fatigue contributes to 20% of road accidents globally.</li>
                <li>Drowsy driving impairs reaction time, similar to driving under the influence.</li>
                <li>Most fatigue-related crashes occur between midnight and 6 AM.</li>
                <li>Long-distance driving without breaks increases drowsiness risk.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_info2:
    st.markdown(
        """
        <div class='info-card'>
            <h4>🛠️ Accident Prevention Tips</h4>
            <ul>
                <li><b>Take Breaks:</b> Stop every 2 hours or 100 miles to rest and stretch.</li>
                <li><b>Stay Hydrated:</b> Drink water to maintain alertness.</li>
                <li><b>Avoid Peak Fatigue Hours:</b> Limit driving between midnight and 6 AM.</li>
                <li><b>Use Alerts:</b> Leverage systems like this to monitor drowsiness.</li>
                <li><b>Share Driving:</b> Alternate drivers on long trips to reduce fatigue.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Feedback Form
st.markdown("<h2 style='text-align: center; color: #006400; font-family: Tahoma, sans-serif;'>Share Your Feedback</h2>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='feedback-form'>", unsafe_allow_html=True)
    st.markdown("<h4>We Value Your Input!</h4>", unsafe_allow_html=True)
    with st.form(key="feedback_form"):
        name = st.text_input("Name", placeholder="Enter your name")
        email = st.text_input("Email", placeholder="Enter your email")
        feedback = st.text_area("Feedback", placeholder="Share your thoughts about the system")
        rating = st.slider("Rate the System (1-5)", min_value=1, max_value=5, value=3)
        submit_button = st.form_submit_button("Submit Feedback", use_container_width=False)
        if submit_button:
            if name and email and feedback:
                st.success("Thank you for your feedback!")
                st.write(f"**Name:** {name}")
                st.write(f"**Email:** {email}")
                st.write(f"**Feedback:** {feedback}")
                st.write(f"**Rating:** {rating}/5")
            else:
                st.error("Please fill out all fields before submitting.")
    st.markdown("</div>", unsafe_allow_html=True)

# Additional Content to Fill Space
st.markdown("<div class='filler-section'><h4>Quick Stats</h4><p>Over 1 million road accidents yearly are linked to driver fatigue. Stay proactive with this system!</p></div>", unsafe_allow_html=True)

# Footer with Contact and Social Links
st.markdown(
    """
    <hr style='margin-top: 3rem;'>
    <div class='footer'>
        <p>© 2025 DrowziGuard | Dissertation Project | By: Arhaan Arif  | BTECH CSE </p>
        <p>
            <a href='mailto:arhaanarifsaifi@gmail.com'>📧 Contact</a> |
            <a href='https://github.com/arhaanarif/DrowziGuard' target='_blank'>🐙 GitHub</a> |
            <a href='https://www.linkedin.com/in/arhaanarif' target='_blank'>💼 LinkedIn</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)