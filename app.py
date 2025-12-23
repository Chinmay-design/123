import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="MES Connect", page_icon="🎓", layout="wide")

# Initialize Session States (Simulated Database)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
if 'confessions' not in st.session_state:
    st.session_state.confessions = [
        {"text": "I hope the hackathon goes well!", "likes": 5, "time": "2023-10-25"},
        {"text": "Does anyone have notes for OS?", "likes": 2, "time": "2023-10-26"}
    ]

# --- LOGIN COMPONENT ---
def login_screen():
    st.title("🛡️ MES Connect Login")
    with st.container(border=True):
        email = st.text_input("Institutional Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("I am a...", ["Student", "Alumni", "Admin"])
        
        if st.button("Sign In", use_container_width=True):
            if "@" in email: # Simple validation
                st.session_state.logged_in = True
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Please enter a valid institutional email.")

# --- DASHBOARDS ---
def student_dashboard():
    st.title("👋 Student Hub")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📢 Announcements")
        st.info("**Academic:** Mid-semester results are out.")
        st.warning("**Event:** Tech Fest registrations close tonight!")
        
        st.subheader("📝 Anonymous Confessions")
        with st.expander("Write a confession..."):
            new_msg = st.text_area("What's on your mind?", label_visibility="collapsed")
            if st.button("Post Anonymously"):
                st.session_state.confessions.insert(0, {"text": new_msg, "likes": 0, "time": str(datetime.now().date())})
                st.success("Posted!")
                st.rerun()
        
        for c in st.session_state.confessions:
            st.chat_message("user", avatar="👻").write(f"{c['text']}  \n*Posted on {c['time']}*")

    with col2:
        st.subheader("🔍 Finders")
        st.button("Find Study Groups")
        st.button("Find Alumni Mentors")
        
def admin_dashboard():
    st.title("⚙️ Admin Command Center")
    st.metric("Active Students", "1,240", "+12%")
    st.metric("Verified Alumni", "450", "+5%")
    
    st.subheader("🚩 Content Moderation")
    for i, c in enumerate(st.session_state.confessions):
        cols = st.columns([3, 1])
        cols[0].write(c['text'])
        if cols[1].button("Delete", key=f"del_{i}"):
            st.session_state.confessions.pop(i)
            st.rerun()

# --- MAIN ROUTING ---
if not st.session_state.logged_in:
    login_screen()
else:
    # Sidebar Navigation
    st.sidebar.title("MES Connect")
    st.sidebar.write(f"Logged in as: **{st.session_state.role}**")
    
    if st.session_state.role == "Student":
        student_dashboard()
    elif st.session_state.role == "Admin":
        admin_dashboard()
    elif st.session_state.role == "Alumni":
        st.title("🤝 Alumni Networking")
        st.write("Welcome back! Here you can connect with students and other alumni.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
