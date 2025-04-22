import streamlit as st
import subprocess
import threading

# Force Streamlit to use a light theme and expand sidebar
st.set_page_config(page_title="Drowsiness Detection Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Light Theme with White Sidebar Text
st.markdown(
    """
    <style>
        /* Force white background for all Streamlit containers */
        body, .stApp, .main, .block-container {
            background-color: #ffffff !important;
            color: #333333 !important;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #005566 !important;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] a {
            color: #ffffff !important;
        }
        
        /* Main Title */
        .main-title {
            text-align: center;
            font-size: 2.8rem;
            color: #005566;
            margin-bottom: 1rem;
        }
        .subheader {
            text-align: center;
            font-size: 1.5rem;
            color: #333333;
            margin-top: 1rem;
        }
        .credit-text {
            text-align: center;
            font-size: 1rem;
            color: #6c757d;
            margin-top: 0.5rem;
            font-style: italic;
        }
        /* News Banner */
        .news-banner {
            width: 100%;
            overflow: hidden;
            background: linear-gradient(90deg, #e6f0fa, #f5f7fa);
            color: #005566;
            font-weight: bold;
            font-size: 1rem;
            padding: 0.8rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
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
        .start-button {
            display: block;
            margin: 0 auto;
            padding: 0.8rem 2rem;
            font-size: 1.2rem;
            font-weight: bold;
            border: 3px solid #ffffff;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: #006400 !important;
            color: #ffffff !important;
        }
        .stop-button {
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
        }
        .start-button:hover {
            background-color: #004d00 !important;
            transform: scale(1.05);
        }
        .stop-button:hover {
            background-color: #f8f9fa !important;
            transform: scale(1.05);
        }
        /* Card Styling */
        .feature-card, .info-card {
            background-color: #f9f9f9;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
            transition: transform 0.3s;
        }
        .feature-card:hover, .info-card:hover {
            transform: translateY(-5px);
        }
        .feature-card h4, .info-card h4 {
            color: #005566;
            margin-bottom: 0.5rem;
        }
        .feature-card p, .info-card p {
            color: #333333;
            font-size: 0.95rem;
        }
        /* Additional Content to Fill Space */
        .filler-section {
            margin-top: 2rem;
            padding: 1rem;
            background-color: #f0f0f0;
            border-radius: 10px;
            text-align: center;
        }
        /* Ensure main content text contrast */
        p, li, h1, h2, h3, h4 {
            color: #333333 !important;
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
            <p>This Driver Drowsiness Detection System uses a deep learning model (MobileNetV2) 
            along with real-time webcam input to monitor a driver's alertness. It detects drowsy 
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

# Main Title
st.markdown("<h1 class='main-title'>Driver Drowsiness Detection System</h1>", unsafe_allow_html=True)

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
              help="Start the drowsiness detection system", 
              use_container_width=False)
else:
    st.button("🛑 Stop Detection", key="stop", on_click=stop_detection, 
              help="Stop the drowsiness detection system", 
              use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #6c757d;'>Built by Arhaan Arif, Enrollment No: 2021-310-043</p>", unsafe_allow_html=True)

# Status Indicator
if st.session_state.detection_running:
    st.markdown("<p style='text-align: center; color: #28a745; font-weight: bold;'>Detection Running...</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align: center; color: #6c757d;'>Detection Stopped</p>", unsafe_allow_html=True)

# Key Features Section
st.markdown("<h2 class='subheader'>Key Features</h2>", unsafe_allow_html=True)
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

# Information Sections
st.markdown("<h2 class='subheader'>Drowsiness & Safety Information</h2>", unsafe_allow_html=True)
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

# Additional Content to Fill Space
st.markdown("<div class='filler-section'><h4>Quick Stats</h4><p>Over 1 million road accidents yearly are linked to driver fatigue. Stay proactive with this system!</p></div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <hr style='margin-top: 3rem;'>
    <p style='text-align: center; color: #6c757d;'>© 2025 Driver Drowsiness Detection System | Major Project | By: Arhaan Arif BTECH CSE 8 SEM SEC-A</p>
    """,
    unsafe_allow_html=True
)