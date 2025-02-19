import gspread
import pandas as pd

# Connect to Google Sheets
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

# Display data for each sheet
for sheet_name, df in data_frames.items():
    print(f"Data from {sheet_name}:")
    print(df.head())
    print("-" * 50)
