# --------------------------------
# main_streamlit.py (Enhanced UI, Modular)
# --------------------------------

import streamlit as st
import cv2
import numpy as np
import time
import autopy
from gesturecontrol import HandDetector


def setup_page():
    """Configure Streamlit page and styles."""
    st.set_page_config(page_title="🖐️ Gesture Mouse", layout="wide", page_icon="🖱️")
    st.markdown(
        """
        <style>
            .main {
                background-color: #f0f2f6;
            }
            .block-container {
                padding-top: 1rem;
            }
            h1 {
                color: #1f4e79;
            }
            .stButton>button {
                border-radius: 8px;
                padding: 0.6rem 1.2rem;
                font-size: 1rem;
            }
            .stSidebar {
                background-color: #ebf3fc;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_controls():
    """Display and return sidebar control values and start/stop flags."""
    st.sidebar.markdown("---")
    start_mouse = st.sidebar.button("🟢 Start Gesture Mouse")
    stop_mouse = st.sidebar.button("🔴 Stop Gesture Mouse")    
    st.sidebar.header("🎛️ Settings")
    wCam = st.sidebar.slider("📷 Webcam Width", 400, 1280, 640)
    hCam = st.sidebar.slider("📷 Webcam Height", 300, 720, 480)
    framR = st.sidebar.slider("🖼️ Control Frame Margin", 20, 200, 100)
    smoothness = st.sidebar.slider("🌀 Mouse Smoothing", 1, 15, 7)
    click_threshold = st.sidebar.slider("🖱️ Click Distance Threshold", 10, 100, 40)



    return wCam, hCam, framR, smoothness, click_threshold, start_mouse, stop_mouse


def add_footer():
    """Add a thin, responsive footer strip with right-side margin."""
    footer_html = """
    <style>

    .footer-thin {
        position: fixed;
        bottom: 0;
        left: 0;
        width: calc(100% - 21rem - 24px);
        margin-left: 21rem;
        margin-right: 24px;
        background-color: #f8f9fa;
        color: #444;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        padding: 8px 20px 8px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;

        /* New: Border and stronger shadow */
        border: 1px solid #ddd;        
        box-shadow: 0 6px 30px rgba(0, 0, 0, 0.12);
        z-index: 1000;

        border-radius: 10px;  /* <-- Rounded corners added */
    }


    .footer-thin .left,
    .footer-thin .center,
    .footer-thin .right {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .footer-thin .center {
        flex-grow: 1;
        justify-content: center;
        text-align: center;
        font-weight: 500;
        color: #333;
    }

    .footer-thin a {
        color: #007ACC;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }

    .footer-thin a:hover {
        color: #005A99;
        text-decoration: underline;
    }

    @media (max-width: 960px) {
        .footer-thin {
            margin-left: 0;
            margin-right: 0;
            width: 100%;
            flex-direction: column;
            padding: 10px 12px;
            gap: 6px;
            text-align: center;
        }

        .footer-thin .left,
        .footer-thin .center,
        .footer-thin .right {
            justify-content: center;
            flex-wrap: wrap;
        }

        .footer-thin .center {
            order: 1;
        }
    }
    </style>

    <div class="footer-thin">
        <div class="left">
            🛠️ <strong>Virtual Gesture Mouse</strong> by 
            <a href="https://www.linkedin.com/in/suraj5424/" target="_blank">Suraj Varma</a> 👨‍💻
        </div>
        <div class="center">
            ✋🖱️ Control your computer with hand gestures • 🚀 2025
        </div>
        <div class="right">
            <a href="https://github.com/suraj5424" target="_blank">💻 GitHub</a>
            <a href="https://linkedin.com/in/suraj5424" target="_blank">🔗 LinkedIn</a>
        </div>
    </div>

    """
    st.markdown(footer_html, unsafe_allow_html=True)



def run_gesture_mouse(wCam, hCam, framR, smoothness, click_threshold, frame_window):
    """Main function to start gesture mouse control."""
    st.success("🟢 Gesture Control Active - Move your hand in the webcam frame.")

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = HandDetector(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.6)
    screen_w, screen_h = autopy.screen.size()

    previous_x, previous_y = 0, 0
    current_x, current_y = 0, 0
    prev_time = 0

    while True:
        success, img = cap.read()
        if not success:
            st.error("Failed to read from webcam.")
            break

        img = detector.find_hands(img, draw=True)
        lm_list, bbox = detector.find_position(img, draw=True)

        if lm_list:
            x1, y1 = lm_list[8][1], lm_list[8][2]  # Index finger tip
            x2, y2 = lm_list[4][1], lm_list[4][2]  # Thumb tip

            fingers = detector.finger_up()

            # Move mouse: Index finger up, middle finger down
            if fingers[1] == 1 and fingers[2] == 0:
                cv2.rectangle(img, (framR, framR), (wCam - framR, hCam - framR), (0, 120, 255), 2)

                x3 = np.interp(x1, (framR, wCam - framR), (0, screen_w))
                y3 = np.interp(y1, (framR, hCam - framR), (0, screen_h))

                current_x = previous_x + (x3 - previous_x) / smoothness
                current_y = previous_y + (y3 - previous_y) / smoothness

                autopy.mouse.move(screen_w - current_x, current_y)
                previous_x, previous_y = current_x, current_y

                cv2.circle(img, (x1, y1), 15, (0, 120, 255), cv2.FILLED)

            # Click: Index finger and thumb up, fingers close together
            if fingers[1] == 1 and fingers[0] == 1:
                length, img, info = detector.find_distance(8, 4, img, draw=True)


                if length < click_threshold:
                    cv2.circle(img, (info[4], info[5]), 15, (200, 0, 255), cv2.FILLED)
                    autopy.mouse.click()

        # Calculate and display FPS
        ctime = time.time()
        fps = 1 / (ctime - prev_time) if ctime - prev_time else 0
        prev_time = ctime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Show image in Streamlit
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame_window.image(img)

        # Break loop on ESC key press (if possible)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()


def main():
    """Main Streamlit app function."""
    setup_page()

    st.title("🖐️ Virtual Mouse using Hand Gestures")
    st.info("Adjust parameters below and press **Start** to control your mouse using hand gestures.")

    add_footer()
    # Initialize session state for mouse control
    if "run_mouse" not in st.session_state:
        st.session_state.run_mouse = False

    wCam, hCam, framR, smoothness, click_threshold, start_mouse, stop_mouse = sidebar_controls()

    if start_mouse:
        st.session_state.run_mouse = True
    if stop_mouse:
        st.session_state.run_mouse = False

    frame_window = st.empty()

    if st.session_state.run_mouse:
        run_gesture_mouse(wCam, hCam, framR, smoothness, click_threshold, frame_window)

if __name__ == "__main__":
    main()

