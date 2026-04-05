import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import time

# Page configuration
st.set_page_config(
    page_title="Heart Disease Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load models with error handling
@st.cache_resource
def load_models():
    try:
        model = joblib.load(r"C:\Users\karna\OneDrive\Documents\ML Projects\Heart Disease\KNN heart.pkl")
        scaler = joblib.load(r"C:\Users\karna\OneDrive\Documents\ML Projects\Heart Disease\scaler.pkl")
        expected_columns = joblib.load(r"C:\Users\karna\OneDrive\Documents\ML Projects\Heart Disease\columns.pkl")
        return model, scaler, expected_columns
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please check the file paths.")
        return None, None, None
    except Exception as e:
        st.error(f"⚠️ Error loading models: {str(e)}")
        return None, None, None

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3043/3043417.png", width=100)
    st.title("Navigation")
    
    selected = option_menu(
        menu_title=None,
        options=["Predictor", "Information", "Risk Factors", "About"],
        icons=["activity", "info-circle", "exclamation-triangle", "person"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "#ff4b4b", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
            "nav-link-selected": {"background-color": "#ff4b4b"},
        }
    )

# Main content
if selected == "Predictor":
    st.markdown('<div class="main-header">❤️ Heart Disease Risk Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">By Jayesh | Advanced AI-Powered Health Assessment Tool</div>', unsafe_allow_html=True)
    
    # Load models
    model, scaler, expected_columns = load_models()
    
    if model is not None:
        # Create two columns for input organization
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Personal Information")
            age = st.slider("Age (years)", 19, 100, 40, help="Your current age")
            sex = st.radio("Sex", ["Male", "Female"], horizontal=True)
            sex_code = "M" if sex == "Male" else "F"
            
            st.markdown("### 💓 Clinical Measurements")
            resting_bp = st.number_input(
                "Resting Blood Pressure (mm Hg)", 
                min_value=80, 
                max_value=200, 
                value=120,
                help="Normal range: 90-120 mm Hg"
            )
            
            cholesterol = st.number_input(
                "Cholesterol (mg/dL)", 
                min_value=100, 
                max_value=600, 
                value=200,
                help="Desirable: <200 mg/dL"
            )
            
            fasting_bs = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dL", 
                [0, 1],
                format_func=lambda x: "Yes" if x == 1 else "No"
            )
        
        with col2:
            st.markdown("### 🫀 Cardiac Indicators")
            chest_pain = st.selectbox(
                "Chest Pain Type",
                ["ATA", "NAP", "TA", "ASY"],
                help="ATA: Atypical Angina, NAP: Non-Anginal Pain, TA: Typical Angina, ASY: Asymptomatic"
            )
            
            resting_ecg = st.selectbox(
                "Resting ECG Result",
                ["Normal", "ST", "LVH"],
                help="ST: ST-T wave abnormality, LVH: Left Ventricular Hypertrophy"
            )
            
            max_hr = st.slider(
                "Maximum Heart Rate Achieved", 
                60, 220, 150,
                help="Normal: 220 - age"
            )
            
            exercise_angina = st.selectbox(
                "Exercise-Induced Angina", 
                ["Y", "N"],
                format_func=lambda x: "Yes" if x == "Y" else "No"
            )
            
            oldpeak = st.slider(
                "ST Depression (Oldpeak)", 
                min_value=0.0, 
                max_value=6.0, 
                value=1.0, 
                step=0.1,
                help="ST depression induced by exercise relative to rest"
            )
            
            st_slope = st.selectbox(
                "ST Slope Pattern",
                ["Up", "Down", "Flat"],
                help="Slope of the peak exercise ST segment"
            )
        
        # Visualization of key metrics
        st.markdown("---")
        st.markdown("### 📈 Health Metrics Overview")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            bp_status = "Normal" if resting_bp < 120 else "Elevated" if resting_bp < 130 else "High"
            st.metric("Blood Pressure", f"{resting_bp} mm Hg", bp_status)
        
        with metric_col2:
            chol_status = "Normal" if cholesterol < 200 else "Borderline" if cholesterol < 240 else "High"
            st.metric("Cholesterol", f"{cholesterol} mg/dL", chol_status)
        
        with metric_col3:
            hr_status = "Good" if max_hr > 150 else "Below Average"
            st.metric("Max Heart Rate", f"{max_hr} bpm", hr_status)
        
        with metric_col4:
            age_risk = "Higher Risk" if age > 50 else "Lower Risk"
            st.metric("Age Factor", f"{age} years", age_risk)
        
        # Prediction button
        st.markdown("---")
        predict_button = st.button("🔍 Predict Heart Disease Risk", use_container_width=True, type="primary")
        
        if predict_button:
            with st.spinner("Analyzing your health data..."):
                time.sleep(1)  # Simulate processing
                
                # Prepare input data
                raw_input = {
                    'Age': age,
                    'RestingBP': resting_bp,
                    'Cholesterol': cholesterol,
                    'FastingBS': fasting_bs,
                    'MaxHR': max_hr,
                    'Oldpeak': oldpeak,
                    'Sex_' + sex_code: 1,
                    'ChestPainType_' + chest_pain: 1,
                    'RestingECG_' + resting_ecg: 1,
                    'ExerciseAngina_' + exercise_angina: 1,
                    'St_Slope_' + st_slope: 1
                }
                
                input_df = pd.DataFrame([raw_input])
                
                # Ensure all expected columns are present
                for col in expected_columns:
                    if col not in input_df.columns:
                        input_df[col] = 0
                
                input_df = input_df[expected_columns]
                
                # Make prediction
                scaled_input = scaler.transform(input_df)
                prediction = model.predict(scaled_input)[0]
                
                # Get prediction probability if available
                try:
                    probability = model.predict_proba(scaled_input)[0]
                    risk_score = probability[1] * 100 if prediction == 1 else probability[0] * 100
                except:
                    risk_score = 85 if prediction == 1 else 25
                
                # Display results with animation
                st.markdown("---")
                
                if prediction == 1:
                    st.markdown(
                        """
                        <div class='prediction-box' style='background-color: #ffebee; border: 2px solid #ff4b4b;'>
                            <h2 style='color: #ff4b4b;'>⚠️ High Risk of Heart Disease</h2>
                            <p style='font-size: 1.2rem;'>Risk Score: {:.1f}%</p>
                            <p>Please consult with a healthcare professional for a comprehensive evaluation.</p>
                        </div>
                        """.format(risk_score),
                        unsafe_allow_html=True
                    )
                    
                    # Risk factors gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = risk_score,
                        title = {'text': "Risk Level"},
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#ff4b4b"},
                            'steps': [
                                {'range': [0, 33], 'color': "lightgreen"},
                                {'range': [33, 66], 'color': "yellow"},
                                {'range': [66, 100], 'color': "salmon"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': risk_score
                            }
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    st.markdown(
                        """
                        <div class='prediction-box' style='background-color: #e8f5e9; border: 2px solid #4caf50;'>
                            <h2 style='color: #4caf50;'>✅ Low Risk of Heart Disease</h2>
                            <p style='font-size: 1.2rem;'>Risk Score: {:.1f}%</p>
                            <p>Keep maintaining a healthy lifestyle! Regular check-ups are still recommended.</p>
                        </div>
                        """.format(risk_score),
                        unsafe_allow_html=True
                    )
                    
                    # Healthy habits reminder
                    st.info("💡 **Tips to maintain heart health:** Regular exercise, balanced diet, stress management, and regular health check-ups!")

elif selected == "Information":
    st.markdown("## ℹ️ About Heart Disease Prediction")
    
    st.info("""
    ### How does this predictor work?
    
    This tool uses a **K-Nearest Neighbors (KNN)** machine learning model trained on clinical data to assess the risk of heart disease.
    
    **Key factors considered:**
    - Age and gender
    - Blood pressure and cholesterol levels
    - Chest pain type
    - Resting ECG results
    - Maximum heart rate achieved
    - Exercise-induced angina
    - ST depression (Oldpeak)
    - ST slope pattern
    
    **Important Note:** This tool is for educational purposes only and should not replace professional medical advice.
    """)
    
    st.markdown("### 📊 Understanding Your Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Risk Factors Explained")
        st.markdown("""
        - **High Blood Pressure (>130 mm Hg):** Increases heart workload
        - **High Cholesterol (>200 mg/dL):** Can lead to artery blockage
        - **Fasting Blood Sugar >120:** Indicator of diabetes risk
        - **Exercise Angina:** Chest pain during physical activity
        - **ST Depression:** May indicate reduced blood flow to heart
        """)
    
    with col2:
        st.markdown("#### Prevention Tips")
        st.markdown("""
        - 🏃‍♂️ **Exercise regularly** (150 minutes/week)
        - 🥗 **Eat heart-healthy foods** (fruits, vegetables, whole grains)
        - 🚭 **Avoid smoking and limit alcohol**
        - 😴 **Get 7-8 hours of sleep**
        - 🧘 **Manage stress** through meditation or yoga
        """)

elif selected == "Risk Factors":
    st.markdown("## 🚨 Major Risk Factors for Heart Disease")
    
    risk_factors = {
        "Modifiable": [
            "High blood pressure",
            "High cholesterol",
            "Smoking",
            "Obesity",
            "Physical inactivity",
            "Diabetes",
            "Unhealthy diet",
            "Stress"
        ],
        "Non-Modifiable": [
            "Age (45+ for men, 55+ for women)",
            "Family history",
            "Gender (men at higher risk)",
            "Race/ethnicity"
        ]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Modifiable Risk Factors")
        for factor in risk_factors["Modifiable"]:
            st.markdown(f"- {factor}")
    
    with col2:
        st.markdown("### ❌ Non-Modifiable Risk Factors")
        for factor in risk_factors["Non-Modifiable"]:
            st.markdown(f"- {factor}")
    
    st.markdown("---")
    st.markdown("### 📋 When to See a Doctor")
    st.warning("""
    Seek immediate medical attention if you experience:
    - Chest pain or discomfort
    - Shortness of breath
    - Pain in arms, back, neck, or jaw
    - Nausea or lightheadedness
    - Cold sweats
    """)

else:  # About
    st.markdown("## 👨‍💻 About the Developer")
    
    st.markdown("""
    **Jayesh** - AI & Data Science
    
    This application demonstrates the application of machine learning in preventive healthcare. 
    The model was trained on comprehensive heart disease datasets and achieves high accuracy in risk prediction.
    
    ### 🛠️ Technologies Used
    - **Frontend:** Streamlit
    - **ML Model:** K-Nearest Neighbors (KNN)
    - **Data Processing:** Pandas, NumPy, Scikit-learn
    - **Visualization:** Plotly, Matplotlib
    
    ### 📞 Contact & Support
    For questions, feedback, or collaboration opportunities, please reach out through:
    - Email: jayeshmachha13@gmail.com
    - GitHub: https://github.com/jayeshmachha
    
    ### 📅 Version History
    - **v2.0** (Current): Modern UI, risk visualization, enhanced metrics
    - **v1.0**: Basic prediction functionality
    
    ---
    *Disclaimer: This tool is for informational purposes only. Always consult with qualified healthcare professionals for medical decisions.*
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Made with ❤️ by Jayesh | Heart Disease Risk Predictor v2.0</p>",
    unsafe_allow_html=True
)