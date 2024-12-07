import streamlit as st
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

# Device configuration
DEVICE = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

# Load the trained model
@st.cache_resource
def load_model():
    num_classes = 1062  # Replace with the actual number of classes
    model = models.resnet50(pretrained=False)  # Same architecture as used during training
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)  # Modify the FC layer
    model.load_state_dict(torch.load("data_augmented_resnet28on50.pth", map_location=DEVICE))
    model = model.to(DEVICE)
    model.eval()  # Set model to evaluation mode
    return model

model = load_model()

# Mapping from class index to hotel ID (from your training code)
index_to_hotel_id = {
    0: 123, 1: 456, 2: 789,  # Replace with actual mapping
    # Continue for all class indices...
}

# Define transformations (same as used during training)
Transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

# Function to predict Top-X hotel IDs for a given image
def predict_topX_hotel_ids(image, top_x=5):
    # Preprocess the image
    image = Transform(image).unsqueeze(0).to(DEVICE)  # Add batch dimension and move to device

    # Perform inference
    with torch.no_grad():
        outputs = model(image)

        # Get the top-X predictions
        _, predicted_topX = outputs.topk(top_x, dim=1, largest=True, sorted=True)
        predicted_topX = predicted_topX.squeeze(0).cpu().numpy()  # Remove batch dimension

    # Map the predicted indices to hotel IDs
    topX_hotel_ids = [index_to_hotel_id[idx] for idx in predicted_topX]
    return topX_hotel_ids

# Streamlit UI
st.title("Hotel Image Classification")
st.write("Upload an image, and the model will predict the top 5 hotel IDs.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("Processing...")

    # Perform prediction
    topX_predictions = predict_topX_hotel_ids(image, top_x=5)
    
    # Display the predictions
    st.write("### Top 5 Predicted Hotel IDs:")
    for rank, hotel_id in enumerate(topX_predictions, start=1):
        st.write(f"{rank}. Hotel ID: {hotel_id}")
