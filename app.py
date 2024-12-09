import streamlit as st
import pandas as pd
from PIL import Image

# Title of the app
st.title("Hotel Image Identifier")

# Step 1: Load Hotel ID CSV (Hidden from the user)

# GitHub raw URL for your CSV file
csv_url = "https://raw.githubusercontent.com/agnitra7/aml_term_project/main/40k_hotel_id_only.csv"

try:
    # Read the CSV from GitHub
    data = pd.read_csv(csv_url)

    # Calculate probabilities for each hotel_id
    hotel_counts = data['hotel_id'].value_counts(normalize=True).reset_index()
    hotel_counts.columns = ['hotel_id', 'probability']

    # Merge probabilities back to the original dataframe
    data = data.merge(hotel_counts, on='hotel_id', how='left')

except Exception as e:
    st.error("Failed to fetch the CSV file. Please check the URL or file format.")
    st.write(e)
    st.stop()

# Step 2: Upload a Hotel Image
st.header("Upload a Hotel Image")
uploaded_image = st.file_uploader("Upload an image of the hotel", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Hotel Image", use_column_width=True)

    # Mockup logic: Select top 5 hotel IDs with the highest probabilities
    # Replace this section with your actual model inference logic
    top_5_hotels = data[['hotel_id']].drop_duplicates().nlargest(5, "probability")

    # Display top 5 hotel IDs (without probabilities)
    st.header("Top 5 Hotel IDs")
    st.write("Here are the top 5 most probable hotel IDs:")
    for index, row in top_5_hotels.iterrows():
        st.write(f"Hotel ID: {row['hotel_id']}")
