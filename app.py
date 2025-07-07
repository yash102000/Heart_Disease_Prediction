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
heart_disease_model = pickle.load(open(f'{working_dir}/models/heart_disease_model.sav', 'rb'))

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
    st.title("Welcome To Heart Disease Prediction Using ML")
    
    # Session state management
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'welcome_shown' not in st.session_state:
        st.session_state.welcome_shown = False
    
    # Welcome page
    if not st.session_state.welcome_shown:
        st.write("This application helps you predict the risk of heart disease based on several health metrics. Please login or register to continue.")
        if st.button("Continue"):
            st.session_state.welcome_shown = True
            st.experimental_rerun()
    
    # Login or Registration
    elif st.session_state.logged_in:
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
    st.markdown("### Chest Pain Type:")
    st.markdown("""
- **0**: Typical angina (chest pain related to decreased blood flow to the heart)
- **1**: Atypical angina (chest pain not directly related to the heart)
- **2**: Non-anginal pain (pain not related to the heart)
- **3**: Asymptomatic (no chest pain)
""")
    cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3])
    
 
    trestbps = st.number_input("Resting Blood Pressure", min_value=50, max_value=200)
    chol = st.number_input("Serum Cholesterol", min_value=100, max_value=600)
    st.markdown("### Fasting Blood Sugar > 120 mg/dl:")
    st.markdown("""
- **0**: Fasting blood sugar <= 120 mg/dl (Normal)
- **1**: Fasting blood sugar > 120 mg/dl (High)
""")
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])
    st.markdown("### Resting Electrocardiographic Results:")
    st.markdown("""
- **0**: Normal
- **1**: ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)
- **2**: Left ventricular hypertrophy (based on Estes' criteria)
""")
    restecg = st.selectbox("Resting Electrocardiographic Results", [0, 1, 2])
    thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220)
    st.markdown("### Exercise Induced Angina:")
    st.markdown("""
- **0**: No (Exercise does not cause angina)
- **1**: Yes (Exercise causes angina)
""")
    exang = st.selectbox("Exercise Induced Angina", [0, 1])
    st.markdown("""
### **Depression Induced by Exercise (Oldpeak)**

Oldpeak refers to the amount of ST depression seen in an ECG during an exercise test. It measures how much the ST segment dips below the baseline, indicating the heart's ability to supply oxygen during physical activity.

- **Low values (0 - 1.0)**: Normal heart response during exercise.
- **Moderate values (1.0 - 2.0)**: Possible reduced blood flow to the heart (ischemia).
- **High values (above 2.0)**: Higher risk of coronary artery disease. Further testing may be needed.
""")

    oldpeak = st.number_input("", min_value=0.0, max_value=6.0)
    st.markdown("### Slope of the Peak Exercise ST Segment:")
    st.markdown("""
- **0**: Upsloping (The ST segment increases with exercise)
- **1**: Flat (The ST segment stays flat with exercise)
- **2**: Downsloping (The ST segment decreases with exercise)
""")
    slope = st.selectbox("Slope of the Peak Exercise ST Segment", [0, 1, 2])
    st.markdown("### Number of Major Vessels Colored by Fluoroscopy:")
    st.markdown("""
- **0**: No major vessels colored (normal)
- **1**: One major coronary artery affected by narrowing or blockages
- **2**: Two major coronary arteries affected by narrowing or blockages
- **3**: Three major coronary arteries affected by narrowing or blockages
""")
    ca = st.selectbox("Number of Major Vessels (0-3)", [0, 1, 2, 3])
    st.markdown("### Thalassemia (Thal):")
    st.markdown("""
- **0**: Normal (No presence of thalassemia)
- **1**: Fixed Defect (Permanent damage or scarring to the heart)
- **2**: Reversible Defect (Heart-related damage that could improve with treatment)
- **3**: Severe Defect (Serious heart defect related to thalassemia)
""")
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
        st.session_state.welcome_shown = False  # Reset welcome page when logged out
        st.success("You have been logged out.")
        st.experimental_rerun()

if __name__ == "__main__":
    main()  # Just call the main function directly
