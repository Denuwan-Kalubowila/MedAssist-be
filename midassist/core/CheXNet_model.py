import os
import django
import numpy as np
import onnxruntime as ort

import cv2
import pathlib
from django.conf import settings
import sys

# Setup Django environment
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midassist.settings')
django.setup()

# Define the ONNX model path
model_path = os.path.join(BASE_DIR, 'models', 'CheXNet.onnx')

def load_model():
    if not os.path.exists(model_path):
        raise ValueError(f"Could not open '{model_path}'")

    # Load the ONNX model using onnxruntime
    session = ort.InferenceSession(model_path)
    return session

# Preprocess the input image
def preprocess_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Resize the image to the required input size of the model (224x224)
    img = cv2.resize(img, (224, 224))

    # Convert the image from BGR (OpenCV format) to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Normalize the image to have values between 0 and 1
    img = img.astype(np.float32) / 255.0

    # Reorder dimensions from (224, 224, 3) to (3, 224, 224)
    img = np.transpose(img, (2, 0, 1))

    # Add a batch dimension (1, 3, 224, 224)
    img = np.expand_dims(img, axis=0)

    return img

def predict_chexnet(image_path):
    session = load_model()
    input_image = preprocess_image(image_path)

    # Run the model on the input image
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    output_data = session.run([output_name], {input_name: input_image})[0]

    # Assuming the output is a classification result
    predicted_class = np.argmax(output_data)

    return predicted_class