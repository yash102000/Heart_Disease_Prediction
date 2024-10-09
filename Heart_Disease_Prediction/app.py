import streamlit as st
import pandas as pd
import pickle
import hashlib
import os

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load the model
working_dir = os.getcwd()  # Get the current working directory
heart_disease_model = pickle.load(open('C:\Users\yashw\OneDrive\Desktop\Heart_Disease_Prediction\models\heart_disease_model.sav', 'rb'))

# User registration and login
def create_user(username, password, email):
    hashed_password = hash_password(password)
    with open("users.txt", "a") as f:
        f.write(f"{username},{hashed_password},{email}\n")  # Save email along with username and password hash

def verify_user(username, password):
    hashed_password = hash_password(password)
    with open("users.txt", "r") as f:
        users = f.readlines()
    for user in users:
        user_info = user.strip().split(",")
        if user_info[0] == username and user_info[1] == hashed_password:
            return True
    return False

def main():
    st.title("Heart Disease Prediction Using ML")
    
    # Session state management
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Login or Registration
    if st.session_state.logged_in:
        show_prediction_page()
    else:
        choice = st.sidebar.selectbox("Login or Register", ["Login", "Register"])

        if choice == "Login":
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.success("Logged in successfully!")
                    show_prediction_page()
                else:
                    st.error("Invalid credentials")

        elif choice == "Register":
            new_user = st.text_input("New Username")
            new_password = st.text_input("New Password", type='password')
            email = st.text_input("Email")  # Add email input
            if st.button("Register"):
                create_user(new_user, new_password, email)  # Pass email to create_user
                st.success("User created successfully!")

def show_prediction_page():
    st.title("Heart Disease Prediction")

    # Input features
    age = st.number_input("Age", min_value=1, max_value=120)
    sex = st.selectbox("Sex", ["Male", "Female"])
    cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
    trestbps = st.number_input("Resting Blood Pressure", min_value=50, max_value=200)
    chol = st.number_input("Serum Cholesterol", min_value=100, max_value=600)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
    restecg = st.selectbox("Resting Electrocardiographic Results", [0, 1, 2])
    thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220)
    exang = st.selectbox("Exercise Induced Angina", [0, 1])
    oldpeak = st.number_input("Depression Induced by Exercise", min_value=0.0, max_value=6.0)
    slope = st.selectbox("Slope of the Peak Exercise ST Segment", [0, 1, 2])
    ca = st.selectbox("Number of Major Vessels (0-3)", [0, 1, 2, 3])
    thal = st.selectbox("Thalassemia", [0, 1, 2, 3])
    target = 1  # Target variable for prediction

    # Create a DataFrame with numerical values for prediction
    input_data = pd.DataFrame([[age, 1 if sex == "Male" else 0, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
                              columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'])

    if st.button("Predict"):
        prediction = heart_disease_model.predict(input_data)
        output = "You have heart disease." if prediction[0] == 1 else "You do not have heart disease."
        st.success(output)

        # Show precautions
        precautions = [
            "Maintain a healthy diet rich in fruits and vegetables.",
            "Engage in regular physical activity.",
            "Avoid smoking and excessive alcohol consumption.",
            "Regular check-ups with your healthcare provider.",
            "Control your cholesterol, blood glucose (sugar), and blood pressure.",
            "Drink alcohol only in moderation.",
            "Get enough sleep."
        ]
        st.subheader("Precautions:")
        for precaution in precautions:
            st.write(f"- {precaution}")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.success("You have been logged out.")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
