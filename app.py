import streamlit as st
from PIL import Image

# Title of the app
st.title("Image Upload and Viewer")

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.success("Image successfully uploaded!")
else:
    st.info("Please upload an image to view it.")
