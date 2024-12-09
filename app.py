import streamlit as st
import pandas as pd
from PIL import Image

# Title of the app
st.title("Hotel Image Identifier")

# Upload CSV file from GitHub
st.header("Step 1: Load Hotel ID Probabilities CSV")
csv_url = "https://raw.githubusercontent.com/agnitra7/main/main/40k_hotel_id_only.csv"  # Replace with your raw URL

try:
    # Load CSV
    data = pd.read_csv(csv_url)
    st.write("CSV loaded successfully! Here's a preview:")
    st.dataframe(data.head())

    # Ensure required columns exist
    if "hotel_id" not in data.columns or "probability" not in data.columns:
        st.error("CSV must contain 'hotel_id' and 'probability' columns.")
        st.stop()
except Exception as e:
    st.error("Failed to load CSV. Please check the URL or file format.")
    st.write(e)
    st.stop()

# Upload image
st.header("Step 2: Upload a Hotel Image")
uploaded_image = st.file_uploader("Upload an image of the hotel", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Hotel Image", use_column_width=True)

    # Mockup logic: Select top 5 hotel IDs with highest probabilities
    # Replace this section with your model inference logic
    st.header("Step 3: Top 5 Hotel IDs")
    top_5_hotels = data.nlargest(5, "probability")

    # Display top 5 hotel IDs
    st.write("Here are the top 5 most probable hotel IDs:")
    st.dataframe(top_5_hotels)

    # Display the results as a list
    for index, row in top_5_hotels.iterrows():
        st.write(f"Hotel ID: {row['hotel_id']} | Probability: {row['probability']:.2f}")
