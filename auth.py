import streamlit as st
import re  #regular expression
import random
import smtplib
from email.mime.text import MIMEText
from database import insert_user, get_user_by_email


# read credentials securely
SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
EMAIL_PASS = st.secrets["EMAIL_PASS"]


# email func
def send_otp_email(receive_email, otp):
    subject = "GyaanSetu Email Verification OTP"
    body = f"Your OTP is: {otp}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receive_email


    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, EMAIL_PASS)
        server.send_message(msg)




# SIGN UP
# @st.dialog("Sign up")

def signup():

    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False

    if "generated_otp" not in st.session_state:
        st.session_state.generated_otp = None


    name = st.text_input("Name")
    email = st.text_input("Email")
    # password = st.text_input("Password", type="password")
    user_class = st.selectbox(
    "Class",
    ["5", "6", "7", "8"],
)


    if not st.session_state.otp_sent:
        if st.button("Send OTP"):

            # Name Validation
            if not name.strip():
                st.error("Name cannot be empty")
                return
            
            # Email validation using regex
            # some.th_ing11@gmail.com
            # @heritageit.edu
            email_pattern = r"^[\w\.-]+@[\w.\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                st.error("Please enter a valid email address")
                return
            



            #genetate 6-digit OTP
            otp = random.randint(100000, 999999)
            st.session_state.generated_otp = otp
            

            # # for demo
            # st.info(f"Demo OTP: {otp}")
            # st.success("OTP sent successfullu!")


            try:
                send_otp_email(email, otp)
                st.session_state.otp_sent = True
                st.success("OTP sent to your email")
            except Exception as e:
                st.error("Failed to send OTP")
                st.write(e)

            


    # OTP verification
    if st.session_state.otp_sent:
        # user_otp = st.text_input("Enter OTP")
        user_otp = st.number_input(
        "Enter OTP",
        min_value=100000,
        max_value=999999,
        format="%d"
    )

        if st.button("Verify OTP"):
            if user_otp == st.session_state.generated_otp:

                if insert_user(name, email, user_class):
                    st.success("Registration Successful")
                    st.session_state.auth_mode = "login"
                else:
                    st.warning("Email already registered")

                st.session_state.otp_sent = False

                # Reset signup state
                st.session_state.otp_sent = False
                st.session_state.generated_otp = None
                
            else:
                st.error("Invalid OTP")

            

            # # password validation
            # errors = []

            # # (i) At least 8 characters
            # if len(password) < 8:
            #     errors.append("Must be at least 8 characters long")

            # # (ii) At least one small letter
            # if not re.search(r'[a-z]', password):
            #     errors.append("Must contain at least one lowercase letter")

            # # (iii) At least one capital letter
            # if not re.search(r'[A-Z]', password):
            #     errors.append("Must contain at least one uppercase letter")

            # # (iv) At least one numeral
            # if not re.search(r'\d', password):  # \d -> contains digit
            #     errors.append("Must contain at least one digit")

            # # (v) At least one special character
            # if not re.search(r'[^a-zA-Z0-9]', password):
            #     errors.append("Must contain at least one special character")

            # # (vi) No space characters
            # if re.search(r'\s', password):  #\s -> contains space
            #     errors.append("Must not contain spaces")

            # # Output result
            # if errors:
            #     for e in errors:
            #             st.error(e)
            # else:
            #     st.success("Password is valid")

            
            


# LOGIN
# @st.dialog("Login")

def login():
    email = st.text_input("Email")

    if st.button("Login"):
        user = get_user_by_email(email)

        if user:
            st.session_state.logged_in = True
            st.session_state.name = user[1]
            st.session_state.email = user[2]
            st.session_state.user_class = user[3]
            st.session_state.points = user[4]
            st.success("Login successful")
            st.rerun()

        else:
            st.error("User not found")



# SINGLE AUTH DIALOG
@st.dialog("Welcome to GyaanSetu")
def auth_dialog():

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    col1, col2, col3 = st.columns([1, 0.2, 1])
    
    with col1:
        if st.button("Login", use_container_width=True):
            st.session_state.auth_mode = "login"
    
    with col2:
        st.write("|")
    
    with col3:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.auth_mode = "signup"

    st.divider()

    # Auth forms based on current mode
    if st.session_state.auth_mode == "login":
        st.subheader("Login")
        login()
    else:
        st.subheader("Sign Up")
        signup()