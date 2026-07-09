import streamlit as st
import pandas as pd
import joblib
import time
from utils.pdf_generator import create_pdf
import plotly.express as px

st.set_page_config(
    page_title = 'Customer Churn Prediction',
    page_icon = '📊',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
)
print(type(st))
print(type(st.session_state))

if "page" not in st.session_state:
    st.session_state.page = 'form'

def show_form():
    #Completion variables for progress tracker and funtion for the status of variables
    if 'customer_completed' not in st.session_state:
        st.session_state.customer_completed = False

    if 'services_completed' not in st.session_state:
        st.session_state.services_completed = False

    if 'account_completed' not in st.session_state:
        st.session_state.account_completed = False

    if 'billing_completed' not in st.session_state:
        st.session_state.billing_completed = False

    def get_status(completed = False, current = False):
        if completed:
            return '🟢'
        elif current:
            return '🟠'
        else:
            return '⚪'
    customer = st.session_state.customer_completed
    services = st.session_state.services_completed
    account = st.session_state.account_completed
    billing = st.session_state.billing_completed

    #Title and caption of the app
    st.title('📊Customer Churn Prediction System')
    st.caption('Predict whether a telecom customer is likely to leave the service') #caption gives a subtle prof.subtitle instead of a heading
    st.divider()
    
    st.subheader('👋 Welcome')
    st.write("Let's get started 😊")
    st.write("Kindly fill the customer details as required 👍🏻")

    #Customer Information
    with st.expander("Customer Information"):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox(
                "Gender",
                ['Female','Male'],
                index = None,
                key = 'gender'
            )

            partner = st.selectbox(
                "Partner",
                ['No', 'Yes'],
                index = None,
                key = 'Partner'
            )

        with col2:
            senior_citizen = st.selectbox(
                "Senior Citizen",
                ['No', 'Yes'],
                index = None,
                key = 'SeniorCitizen'
            )
            senior = 1 if senior_citizen == 'Yes' else 0
    
            dependents = st.selectbox(
                "Dependents",
                ['No', 'Yes'],
                index = None,
                key = 'Dependents'
            )

        customer = all([gender is not None, 
                        partner is not None,
                        dependents is not None,
                        senior_citizen is not None])

    #Service Information
    with st.expander("Service Information"):
        with st.expander('📞Connectivity'):
            col1, col2 = st.columns(2)
            with col1:
                phone_service = st.selectbox(
                    "Phone Service",
                    ['No', 'Yes'],
                    index = None,
                    key = 'PhoneService'
                )

                internet_service = st.selectbox(
                    "Internet Service",
                    ['No', 'DSL', 'Fiber Optic'],
                    index = None,
                    key = 'InternetService'
                )

            with col2:
                multiple_lines = st.selectbox(
                    "Multiple Lines",
                    ['No phone service', 'No', 'Yes'],
                    index = None,
                    key = 'MultipleLines'
                )

        with st.expander('🔒Internet Features'):
            col1, col2 = st.columns(2)
            with col1: 
                online_security = st.selectbox(
                    "Online Security",
                    ['No internet service', 'No', 'Yes'],
                    index = None,
                    key = 'OnlineSecurity'
                )

                device_protection = st.selectbox(
                    "Device Protection",
                    ['No internet service', 'No', 'Yes'],
                    index = None,
                    key = 'DeviceProtection'
                ) 

            with col2:
                online_backup = st.selectbox(
                    "Online Backup",
                    ['No internet service', 'No', 'Yes'],
                    index = None,
                    key = 'OnlineBackup'
                )

                tech_support = st.selectbox(
                    "Tech Support",
                    ['No internet service', 'No', 'Yes'],
                    index = None,
                    key = 'TechSupport'
                )

        with st.expander("🎭Entertainment"):
            col1, col2 = st.columns(2)
            with col1:
                streaming_tv = st.selectbox(
                    "Streaming TV",
                    ['No internet service','No', 'Yes'],
                    index = None,
                    key = 'StreamingTV'
                )
        
            with col2:
                streaming_movies = st.selectbox(
                    "Streaming Movies",
                    ['No internet service', 'No', 'Yes'],
                    index = None,
                    key = 'StreamingMovies'
                )

        services = all([phone_service is not None,
                        multiple_lines is not None,
                        internet_service is not None,
                        online_security is not None,
                        online_backup is not None,
                        device_protection is not None,
                        tech_support is not None,
                        streaming_tv is not None,
                        streaming_movies is not None])


    #Billing and Account Information
    with st.expander("Billing and Account Information"):
        with st.expander('🧾Account Details'):
            contract = st.selectbox(
                "Contract",
                ['Month-to-month','One year', 'Two year'],
                index = None,
                key = 'Contract'
            )
        
            tenure = st.slider(
                "📅Tenure(Months)",
                min_value = 0,
                max_value = 72,
                value = 12,
                key = 'Tenure'
            )

        account = all([contract is not None,
                       tenure is not None])
    
        with st.expander('💳Billing Details'):
            col1, col2 = st.columns(2)
            with col1:
                paperless_billing = st.selectbox(
                    "📄Paperless Billing",
                    ['No','Yes'],
                    index = None,
                    key = 'PaperlessBilling'
                )
            
                monthly_charges = st.slider(
                    "💰Monthly Charges",
                     min_value = 18.0,
                    max_value = 120.0,
                    value = 70.0,
                    step = 0.5,
                    key = 'MonthlyCharges'
                )

            with col2:
                payment_method = st.selectbox(
                    "💳Payment Method",
                    ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'],
                    index = None,
                    key = 'PaymentMethod'
                )

                total_charges = st.number_input(
                    "💸Total Charges",
                    min_value = 0.0,
                    value = 1000.0,
                    step = 10.0,
                    key = 'TotalCharges',
                    help = 'Enter the total amount the customer has paid so far.'
                )

        billing = all([paperless_billing is not None,
                       payment_method is not None,
                       monthly_charges is not None,
                       total_charges is not None])

    current_customer = not customer
    current_services = customer and not services
    current_account = customer and services and not account
    current_billing = customer and services and account and not billing
    ready = customer and services and account and billing
    prediction_status = '🚀 Ready to predict' if ready else '🔒 Prediction'

    #save all the input data inside a dictionary for future use
    input_data = {'gender': gender, 
                  'SeniorCitizen': senior, 
                  'Partner': partner, 
                  'Dependents': dependents,
                  'tenure': tenure, 
                  'PhoneService': phone_service, 
                  'MultipleLines': multiple_lines, 
                  'InternetService': internet_service,
                  'OnlineSecurity': online_security, 
                  'OnlineBackup': online_backup, 
                  'DeviceProtection': device_protection, 
                  'TechSupport': tech_support, 
                  'StreamingTV': streaming_tv, 
                  'StreamingMovies': streaming_movies, 
                  'Contract': contract,
                  'PaperlessBilling': paperless_billing, 
                  'PaymentMethod': payment_method,
                  'MonthlyCharges': monthly_charges, 
                  'TotalCharges': total_charges
                 }
    st.session_state.input_data = input_data

    #Create a copy of input_data for pdf report generation
    report_data = input_data.copy()
    report_data['SeniorCitizen'] = (
        'Yes' if report_data['SeniorCitizen'] == 1 else 'No'
    )
    st.session_state.report_data = report_data


    with st.sidebar:
        st.markdown('## 🚀 Prediction Journey')
        progress_placeholder = st.empty()

        progress_placeholder.markdown(f"""
        <h3> 📋Progress </h3>
        <p>{get_status(customer, current_customer)} 
        <b>Customer Information </b></p>
    
        <p>{get_status(services, current_services)}
        <b>Service Information </b></p>
    
        <p>{get_status(account, current_account)}
        <b>Account Details </b></p>
    
        <p>{get_status(billing, current_billing)}
        <b>Billing Details </b></p>

        <hr>

        <p>{prediction_status}<p/>
        """, unsafe_allow_html = True)

        with st.expander('Navigation Menu'):
            with st.expander('Objectives'):
                st.info('Help the Users to predict customer churn based on customer information.')

            with st.expander('Model Information'):
                st.info('This application is using Random Forest model for predicting Customer Churn.')
                st.info('Used dataset for training: IBM Telco Dataset')
                st.info('The Dataset mostly contains Binary Classification')
        
            with st.expander('Developer'):
                st.info('Developed by: Dhruv Mathur')

            with st.expander('Version'):
                st.info('1.0')

    if st.button("📋Review Details", disabled = not ready):
        st.session_state.page = 'review'
        st.rerun()
            
def show_review():
    input_data = st.session_state.input_data
    st.balloons()
    st.title("📋 Review details")
    st.markdown('''
    Please verify all the information below before generating the prediction.
    If you notice any mistake, simply click **Edit Details**.
    ''')
    
    with st.expander('👤Customer Information', expanded = True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Gender**')
            st.markdown('**Partner**')
            st.markdown('**Dependents**')
            st.markdown('**Senior Citizen**')

        with col2:
            st.write(input_data['gender'])
            st.write(input_data['Partner'])
            st.write(input_data['Dependents'])
            st.write('Yes' if input_data['SeniorCitizen'] == 1 else 'No')

    with st.expander('📞Service Information', expanded = True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Phone Service**')
            st.markdown('**Multiple Lines**')
            st.markdown('**Internet Service**')
            st.markdown('**Online Security**')
            st.markdown('**Online Backup**')
            st.markdown('**Device Protection**')
            st.markdown('**Tech Support**')
            st.markdown('**Streaming TV**')
            st.markdown('**Streaming Movies**')

        with col2:
            st.write(input_data['PhoneService'])
            st.write(input_data['MultipleLines'])
            st.write(input_data['InternetService'])
            st.write(input_data['OnlineSecurity'])
            st.write(input_data['OnlineBackup'])
            st.write(input_data['DeviceProtection'])
            st.write(input_data['TechSupport'])
            st.write(input_data['StreamingTV'])
            st.write(input_data['StreamingMovies'])

    with st.expander('💳Account Details', expanded = True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Contract**')
            st.markdown('**Tenure**')

        with col2:
            st.write(input_data['Contract'])
            st.write(input_data['tenure'])

    with st.expander('💰Billing Details', expanded = True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('**Paperless Billing**')
            st.markdown('**Payment Method**')
            st.markdown('**Monthly Charges**')
            st.markdown('**Total Charges**')

        with col2:
            st.write(input_data['PaperlessBilling'])
            st.write(input_data['PaymentMethod'])
            st.write(input_data['MonthlyCharges'])
            st.write(input_data['TotalCharges'])
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝Edit Details", use_container_width = True):            
            st.session_state.page = 'form'

    with col2:
        if st.button("✅ Confirm & Predict", use_container_width = True):
            st.session_state.page = 'prediction_engine'
            st.session_state.prediction_started = False
            st.rerun()

    st.success("🎉Great!\nYou've completed all required information\n\nPlease review everything carefully before generating the prediction.")
            
def show_prediction_engine():
    if not st.session_state.prediction_started:
        st.title("🤖 AI Prediction Engine")
        st.info('Initializing prediction engine...')
        st.markdown("###Please wait while we analyze the customer's profile...")
        progress = st.progress(0)
        status = st.empty()

        steps = [
            "🔍 Validating customer profile...",
            "🧠 Preparing machine learning pipeline...",
            "🌲 Running random Forest model...",
            "📊 calculating churn probability...",
            "💡 Generating recommendations..."
        ]

        for i, step in enumerate(steps):
            status.info(step)
            progress.progress((i + 1) * 20)
            time.sleep(1.1)

        st.success("All tasks completed!")
        time.sleep(3)

        input_df = pd.DataFrame([st.session_state.input_data])
        rf_pipeline = joblib.load("models/customer_churn_pipeline.pkl")

        prediction = rf_pipeline.predict(input_df)[0]    
        probability = rf_pipeline.predict_proba(input_df)[0]
        st.session_state.prediction = prediction
        st.session_state.probability = probability

        st.session_state.prediction_started = True
        st.rerun()

    st.session_state.page = "prediction_result"
    st.rerun()

def show_prediction_result():
    st.title("🤖Customer Churn Prediction Report")
    status = st.empty()
    status.success("✅ Prediction completed successfully!")
    time.sleep(0.3)

    input_data = st.session_state.input_data
    prediction = st.session_state.prediction
    probability = st.session_state.probability
    confidence = max(probability) * 100
    
    if prediction == 0:            
        st.success(
            f"""
            🟢CUSTOMER IS LIKELY TO STAY \n
            Confidence : {confidence:.2f}%
            """)
    else:
        st.error(
            f"""
            🔴CUSTOMER IS LIKELY TO LEAVE THE SERVICE \n
            Confidence : {confidence:.2f}%
            """)

    stay_prob = probability[0]
    churn_prob = probability[1]

    if prediction == 0:
        cards = [
            ("🟢 Alternative Outcome", stay_prob),
            ("🔴 Primary Prediction", churn_prob)
        ]
    else:
        cards = [
            ("🔴 Primary Prediction", churn_prob),
            ("🟢 Alternative Outcome", stay_prob)
        ]
    st.markdown('---')
    st.header("📊 Prediction Confidence")
    
    col1, col2 = st.columns(2)
    for col, (title, value) in zip([col1,col2], cards):
        with col:
            st.subheader(title)
            st.metric(
                "Probability",
                f"{value * 100:.2f}%"
            )
            st.progress(value)

    chart_df = pd.DataFrame({
        'Prediction': ['Stay','Leave'],
        'Probability': [probability[0] *100, probability[1]*100],
    })
    fig = px.pie(chart_df,
                 names = 'Prediction',
                 values = 'Probability',
                 hole = 0.45,
                 title = 'Prediction Probability Distribution'
                ).update_traces(textinfo = 'percent+label').update_layout(title_x = 0.5)
    
    st.plotly_chart(fig, use_container_width = True)
    
    st.subheader('💡Recommendations')
    recommendations = []
    if input_data['Contract'] == 'Month-to-month':
        recommendations.append('Offer a yearly contract with discounts.')

    if input_data['TechSupport'] == 'No':
        recommendations.append('Offer technical support services.')

    if input_data['OnlineSecurity'] == 'No':
        recommendations.append('Recommend Online Security.')

    if input_data['PaperlessBilling'] == 'Yes':
        recommendations.append('Send loyalty emails to improve engagement.')

    if input_data['PaymentMethod'] == 'Electronic Check':
        recommendations.append('Recommend automatic payment methods.')
    loyal = 'Customer looks loyal! Keep providing quality service.'


    #check prediction and display recommendation
    if prediction == 1:
        st.warning('Immediate retention strategy is recommended.')
        for rec in recommendations:
            st.info(rec)
    else:
        st.success(loyal)

    #Final Buttons
    col1, col2, col3 = st.columns(3)
    with col1:    
        if st.button("⬅️ Edit Details", use_container_width = True):
            st.session_state.page = 'review'
            st.rerun()
        
    with col2:
        report_data = st.session_state.report_data
        create_pdf(report_data,
                   prediction,
                   confidence,
                   recommendations,
                   loyal)
        
        with open('Customer_Churn_Report.pdf', 'rb') as file:
            pdf_data = file.read()
            
        st.download_button("📃 Download Report", data = pdf_data,
                          file_name = 'Customer_Churn_Report.pdf',
                          mime = "application/pdf",
                          use_container_width = True)

    with col3:
        if st.button("🏠Finish", use_container_width = True):
            st.balloons()
            st.success("""
            ###🎉Thank You! \n
            Thank You for using the Customer Churn Prediction System.\n
            We hope this analysis helped you understand the customer's retention risk.\n
            Have A Wonderful Day! 😉👋
            """)
            time.sleep(6)

            st.session_state.clear()
            st.session_state.page = 'form'
            st.rerun()
    
if st.session_state.page == 'form':
    show_form()

elif st.session_state.page == 'review':
    show_review()

elif st.session_state.page == 'prediction_engine':
    show_prediction_engine()

elif st.session_state.page == 'prediction_result':
    show_prediction_result()