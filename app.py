import streamlit as st
from PIL import Image
import torch
from torchvision import transforms
import torch.nn as nn


# Load the trained ResNet model
# Replace 'your_model.pth' with the path to your saved model
import gdown

@st.cache(allow_output_mutation=True)
def download_and_load_model():
    url = "https://drive.google.com/file/d/102SWcrMM9FOzvW7xZOjRwS-00lADd4zH/view?usp=drive_link"  # Replace YOUR_FILE_ID
    output = "model.pth"
    gdown.download(url, output, quiet=False)
    model = torch.load(output, map_location=torch.device("cpu"))
    model.eval()
    return model

model = download_and_load_model()

# Define image preprocessing steps
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize to match ResNet input size
    transforms.ToTensor(),  # Convert to Tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize for pretrained models
])

# Streamlit UI
st.title("Hotel Image Classifier")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Preprocess the image
    input_tensor = preprocess(image).unsqueeze(0)  # Add batch dimension

    # Predict using the model
    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = torch.argmax(output, dim=1).item()  # Get the class ID

    # Display the result
    st.success(f"The predicted hotel ID is: {predicted_class}")
else:
    st.info("Please upload an image to classify.")
