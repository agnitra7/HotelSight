import streamlit as st
from PIL import Image

# Title of the Streamlit app
st.title("Image Upload and Viewer")

# File uploader for image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded file details
    st.write("Uploaded File Details:")
    st.write(f"File Name: {uploaded_file.name}")
    st.write(f"File Type: {uploaded_file.type}")
    st.write(f"File Size: {uploaded_file.size} bytes")

    # Open the image file using PIL
    image = Image.open(uploaded_file)

    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
