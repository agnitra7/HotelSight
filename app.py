import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np

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

    # Step 3: Select top 20 and randomly pick 5 based on probabilities
    # Get top 20 hotel_ids based on probabilities
    top_20_hotels = data[['hotel_id', 'probability']].drop_duplicates().nlargest(20, "probability")

    # Randomly sample 5 hotel_ids from the top 20 using their probabilities as weights
    sampled_hotels = top_20_hotels.sample(
        n=5,
        weights="probability",
        random_state=np.random.randint(0, 1000)  # Ensure reproducibility for debugging
    )

    # Display top 5 randomly sampled hotel IDs
    st.header("Top 5 Hotel IDs (Randomly Selected from Top 20)")
    st.write("Here are the top 5 randomly selected hotel IDs:")
    for index, row in sampled_hotels.iterrows():
        st.write(f"Hotel ID: {row['hotel_id']}")
