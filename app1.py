import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from PIL import Image
import altair as alt  # Import Altair for interactive charts

# --- Sample Data (replace with real data later) ---
crop_data = pd.DataFrame({
    'Crop': ['Rice', 'Wheat', 'Maize', 'Cotton', 'Soybean'],
    'Yield': [5.5, 4.8, 7.2, 3.5, 5.0],  # tons per hectare
    'Price': [1200, 1000, 1500, 1100, 1300],  # per ton
    'Moisture_Optimal': [40, 35, 50, 30, 45],
    'Temperature_Optimal': [25, 20, 28, 22, 27],
    'Rainfall_Optimal': [10, 5, 15, 8, 12]
})

sensor_data = pd.DataFrame({
    'Date': pd.to_datetime(['2023-10-26', '2023-10-27', '2023-10-28', '2023-10-29', '2023-10-30']),
    'Moisture': np.random.uniform(low=30, high=60, size=5),
    'Temperature': np.random.uniform(low=20, high=30, size=5),
    'Light': np.random.uniform(low=400, high=800, size=5),
    'Disease_Risk': np.random.randint(low=1, high=6, size=5)
})

# --- Functions ---
def get_crop_recommendations(soil_type, weather):
    """Simulates crop recommendations based on soil type and weather."""
    recommended_crops = []
    for index, crop in crop_data.iterrows():
        if soil_type == 'Loamy':
            if (abs(weather['Temperature'] - crop['Temperature_Optimal']) <= 5 and 
                abs(weather['Rainfall'] - crop['Rainfall_Optimal']) <= 3):
                recommended_crops.append(crop['Crop'])
    return recommended_crops

def predict_crop_yield(crop, moisture, temperature, rainfall):
    """Simulates crop yield prediction using linear regression."""
    X = np.array([moisture, temperature, rainfall]).reshape(1, -1)
    model = LinearRegression()
    model.fit(crop_data[['Moisture_Optimal', 'Temperature_Optimal', 'Rainfall_Optimal']], crop_data['Yield'])
    predicted_yield = model.predict(X)[0]
    return predicted_yield

def plot_sensor_data(data):
    """Plots sensor data over time."""
    fig, axs = plt.subplots(2, 2, figsize=(12, 6))
    axs[0, 0].plot(data['Date'], data['Moisture'], label='Moisture')
    axs[0, 0].set_ylabel('Moisture (%)')
    axs[0, 0].legend()
    axs[0, 1].plot(data['Date'], data['Temperature'], label='Temperature')
    axs[0, 1].set_ylabel('Temperature (°C)')
    axs[0, 1].legend()
    axs[1, 0].plot(data['Date'], data['Light'], label='Light')
    axs[1, 0].set_ylabel('Light Intensity (lux)')
    axs[1, 0].legend()
    axs[1, 1].plot(data['Date'], data['Disease_Risk'], label='Disease Risk')
    axs[1, 1].set_ylabel('Disease Risk (1-5)')
    axs[1, 1].legend()
    plt.tight_layout()
    st.pyplot(fig)

def simulate_market_data():
    """Simulates market price data."""
    # You'd replace this with real data from APIs or external sources
    market_data = pd.DataFrame({
        'Date': pd.to_datetime(['2023-10-26', '2023-10-27', '2023-10-28', '2023-10-29', '2023-10-30']),
        'Rice': np.random.uniform(low=1100, high=1300, size=5),
        'Wheat': np.random.uniform(low=900, high=1100, size=5),
        'Maize': np.random.uniform(low=1400, high=1600, size=5),
        'Cotton': np.random.uniform(low=1000, high=1200, size=5),
        'Soybean': np.random.uniform(low=1200, high=1400, size=5)
    })
    return market_data

def generate_weather_alerts(location):
    """Simulates weather alerts based on location (placeholder)."""
    # This is a placeholder for real weather APIs.
    alerts = []
    if location == 'Chennai':
        alerts.append("Heavy rain expected in the next 24 hours. Take precautions.")
    return alerts

def recommend_waste_management(crop_waste):
    """Simulates waste management recommendations based on crop waste type."""
    # You'd replace this with real data on waste recycling options and businesses
    recommendations = {}
    if crop_waste == 'Rice Husk':
        recommendations['options'] = ['Composting', 'Biofuel production', 'Animal feed']
        recommendations['businesses'] = ['ABC Compost', 'Green Energy Solutions']
    return recommendations

def detect_crop_threats(crop_image):
    """Simulates crop threat detection using image recognition (placeholder)."""
    # This would use a real image recognition model in a real application
    if crop_image == 'image_with_disease':
        return "Disease detected! Consider applying treatment."
    else:
        return "No threats detected."

# --- Streamlit App ---
st.set_page_config(layout="wide") # Enable full width layout

st.title('Comprehensive AgroSense - Smart Agriculture Platform')

# --- 1. Crop Selection & Analysis ---
with st.container():
    st.header("Crop Selection & Analysis")
    st.markdown("Choose your soil type and enter current weather data:")
    col1, col2 = st.columns(2) 
    with col1:
        soil_type = st.selectbox("Soil Type", ['Loamy', 'Sandy', 'Clayey'])
        temperature = st.number_input("Temperature (°C)", min_value=0, max_value=40, value=25, key='temperature_input')
    with col2:
        rainfall = st.number_input("Rainfall (mm)", min_value=0, max_value=50, value=10, key='rainfall_input')
    
    weather = {'Temperature': temperature, 'Rainfall': rainfall} # Define the weather dictionary here

    recommended_crops = get_crop_recommendations(soil_type, weather)
    if recommended_crops:
        st.success(f"Recommended crops: {', '.join(recommended_crops)}")
    else:
        st.warning("No crops recommended based on current conditions. Consider adjusting soil type or weather.")

    st.dataframe(crop_data)

# --- 2. Crop Monitoring & Management ---

with st.container():
    st.header("Crop Monitoring & Management")
    st.markdown("Current sensor readings:")

    plot_sensor_data(sensor_data) # Plot sensor data

    # Interactive Chart with Altair
    st.subheader("Interactive Sensor Data Visualization")
    chart_data = sensor_data.melt(id_vars='Date', value_vars=['Moisture', 'Temperature', 'Light', 'Disease_Risk'])
    chart = alt.Chart(chart_data).mark_line().encode(
        x='Date:T',
        y='value:Q',
        color='variable:N'
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

# --- 3. Yield Prediction ---
with st.container():
    st.header("Crop Yield Prediction")
    selected_crop = st.selectbox("Select Crop", crop_data['Crop'])
    col1, col2, col3 = st.columns(3)
    with col1:
        moisture = st.number_input("Moisture (%)", min_value=0, max_value=100, value=50, key='moisture_input')
    with col2:
        temperature = st.number_input("Temperature (°C)", min_value=0, max_value=40, value=25, key='temp_input')
    with col3:
        rainfall = st.number_input("Rainfall (mm)", min_value=0, max_value=50, value=10, key='rain_input')

    predicted_yield = predict_crop_yield(selected_crop, moisture, temperature, rainfall)
    st.success(f"Predicted Yield for {selected_crop}: {predicted_yield:.2f} tons/hectare")

    #  Add a chart to visualize predicted yield vs. actual yield
    st.subheader("Visualize Predicted vs. Actual Yield (coming soon)")
    # ... (You could implement this with a bar chart or a line chart that compares the two values)

# --- 4. Market Analysis ---
with st.container():
    st.header("Market Analysis & Price Trends")
    st.markdown("Current market prices for your crops:")

    market_data = simulate_market_data()
    st.dataframe(market_data) # Display market data table

    # Interactive Chart with Altair
    st.subheader("Interactive Market Price Visualization")
    market_chart_data = market_data.melt(id_vars='Date', value_vars=market_data.columns[1:])
    market_chart = alt.Chart(market_chart_data).mark_line().encode(
        x='Date:T',
        y='value:Q',
        color='variable:N'
    ).interactive()
    st.altair_chart(market_chart, use_container_width=True)

# --- 5. Disaster Management ---
with st.container():
    st.header("Disaster Management")
    location = st.text_input("Enter your location:")
    if location:
        alerts = generate_weather_alerts(location)
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.info("No weather alerts for your location at this time.")

    # (You could integrate a map, weather radar visualization, or disaster preparedness information here)

# --- 6. Waste Management & Monetization ---
with st.container():
    st.header("Waste Management & Monetization")
    crop_waste = st.selectbox("Select crop waste type", ['Rice Husk', 'Wheat Straw', 'Cotton Stalks'])
    if crop_waste:
        recommendations = recommend_waste_management(crop_waste)
        if recommendations:
            st.info(f"Waste management options for {crop_waste}:")
            st.write(f" - {', '.join(recommendations['options'])}")
            st.write("Connecting you with businesses:")
            for business in recommendations['businesses']:
                st.write(f" - {business}")
        else:
            st.info("No specific recommendations available for this crop waste type yet.")

# --- 7. Threat Management & Prevention ---
with st.container():
    st.header("Threat Management & Prevention")
    st.markdown("Upload a photo of your crop to check for potential threats.")

    uploaded_image = st.file_uploader("Upload Crop Image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image) 
        st.info(detect_crop_threats('image_with_disease')) # Simulate image recognition

# --- Conclusion ---
st.markdown("---")
st.write("This is a prototype of the Comprehensive AgroSense platform. It demonstrates the core features and capabilities. In the full version, you'd have access to detailed data analysis, actionable insights, and automation features.")