import streamlit as st
import pandas as pd
import gspread
import plotly.express as px
from datetime import datetime, timedelta

# Connect to Google Sheets function
def get_google_sheets_data(sheet_name: str):
    """Fetches data from Google Sheets and returns it as a Pandas DataFrame."""
    gc = gspread.service_account(filename="google_service_account.json")  # Update with your file
    sheet = gc.open("Athlete Wellness Tracker").worksheet(sheet_name)  # Update with your sheet name
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Fetch multiple data sheets
sheet_names = ["HydrationLogs", "NutritionLogs", "WeightLogs"]  # Add more sheet names as needed
data_frames = {}

# Loop through each sheet and store the DataFrame
for sheet_name in sheet_names:
    data_frames[sheet_name] = get_google_sheets_data(sheet_name)

# Title of the Dashboard
st.title("Athlete Wellness Tracker Dashboard")

# Fetch Athlete Names for Filtering (Only one athlete at a time)
athletes = data_frames["NutritionLogs"]["Athlete"].unique()  # Replace with the actual column name for athletes

# Athlete Filter (Single Athlete)
selected_athlete = st.selectbox("Select Athlete", athletes)

# Date Range Filter
# Set start_date to be 2 weeks ago from the current date
default_start_date = datetime.today() - timedelta(weeks=2)
start_date, end_date = st.date_input(
    "Select Date Range", 
    value=(default_start_date, datetime.today())
)

def filter_data(df, selected_athlete, start_date, end_date):
    # Convert start_date and end_date to datetime64
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df["Date"] = pd.to_datetime(df["Date"])  # Ensure Date is in datetime format
    filtered_df = df[df["Athlete"] == selected_athlete]  # Filter by selected athlete
    filtered_df = filtered_df[(filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)]  # Filter by date range
    return filtered_df


# Data Charts for Nutrition, Hydration, and Weight Logs
# Nutrition Data Chart (Multi-line chart for Protein, Carbs, Fats, etc.)
if "NutritionLogs" in data_frames:
    st.subheader(f"Nutritional Intake Over Time for {selected_athlete}")
    
    # Get nutrition data from the data_frames dictionary and filter it by selected athlete and date range
    nutrition_df = data_frames["NutritionLogs"]
    nutrition_df = filter_data(nutrition_df, selected_athlete, start_date, end_date)
    
    # Set Date as index for plotting
    nutrition_df.set_index("Date", inplace=True)
    
    # Checkbox to toggle data labels
    show_data_labels = st.checkbox("Show Data Labels on Chart", value=True)

    # Plot Multi-line chart using Plotly
    fig_nutrition = px.line(
        nutrition_df,
        x=nutrition_df.index,  # Use the Date as the x-axis
        y=["Protein (g)", "Carbs (g)", "Fats (g)", "Sodium (mg)", "Potassium (mg)"],  # Plot these nutrients
        labels={"value": "Nutrient Value", "variable": "Nutrient"},
        title=f"Nutritional Intake for {selected_athlete}",
        template="plotly_dark"  # Optional: Customize the theme
    )
    
    # Add data labels to each point if the checkbox is checked
    if show_data_labels:
        for trace in fig_nutrition.data:
            trace.update(mode="lines+markers+text", textposition="top center", text=trace.y)
    
    # Show the nutrition chart
    st.plotly_chart(fig_nutrition)
    
    # Hydration Data Chart (Single line)
    if "HydrationLogs" in data_frames:
        st.subheader(f"Hydration Levels Over Time for {selected_athlete}")
        hydration_df = data_frames["HydrationLogs"]
        hydration_df = filter_data(hydration_df, selected_athlete, start_date, end_date)
        
        fig_hydration = px.line(
            hydration_df, 
            x="Date", 
            y="Hydration Level",  # Replace with your actual hydration column name
            labels={"Date": "Date", "Hydration Level": "Hydration Level (L)"}  # Adjust label accordingly
        )
        
        # Add data labels to each point if the checkbox is checked
        if show_data_labels:
            for trace in fig_hydration.data:
                trace.update(mode="lines+markers+text", textposition="top center", text=trace.y)

        st.plotly_chart(fig_hydration)

    # Weight Data Chart (Single line)
    if "WeightLogs" in data_frames:
        st.subheader(f"Weight Over Time for {selected_athlete}")
        weight_df = data_frames["WeightLogs"]
        weight_df = filter_data(weight_df, selected_athlete, start_date, end_date)
        
        fig_weight = px.line(
            weight_df, 
            x="Date", 
            y="Weight (kg)",  # Replace with your actual weight column name
            labels={"Date": "Date", "Weight (kg)": "Weight (kg)"}  # Adjust label accordingly
        )
        
        # Add data labels to each point if the checkbox is checked
        if show_data_labels:
            for trace in fig_weight.data:
                trace.update(mode="lines+markers+text", textposition="top center", text=trace.y)

        st.plotly_chart(fig_weight)
