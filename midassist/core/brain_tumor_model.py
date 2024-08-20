import os
import django
import numpy as np
import tensorflow as tf
import cv2
import pathlib

from django.conf import settings

import sys
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
# Ensure Django settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midassist.settings')
django.setup()


def load_interpreter():
    model_path = settings.MODEL_PATH
    if not os.path.exists(model_path):
        raise ValueError(f"Could not open '{model_path}'")

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    return interpreter


# Preprocess the input image
def preprocess_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Resize the image to the required input size of the model (150x150)
    img = cv2.resize(img, (150, 150))

    # Normalize the image to have values between 0 and 1
    img = img.astype(np.float32) / 255.0

    # Add a batch dimension (1, 150, 150, 3)
    img = np.expand_dims(img, axis=0)

    return img


def predict(image_path):
    interpreter = load_interpreter()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_image = preprocess_image(image_path)
    interpreter.set_tensor(input_details[0]['index'], input_image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output_data)
    return predicted_class

# image_path = "../media/post_images/41598_2023_41576_Fig1_HTML.jpg"  # Replace with the path to your image
# input_image = preprocess_image(image_path)
# predict(image_path)

# # Set the input tensor
# interpreter.set_tensor(input_details[0]['index'], input_image)
#
# # Invoke the interpreter
# interpreter.invoke()
#
# # Get the output tensor
# output_data = interpreter.get_tensor(output_details[0]['index'])
#
# # Print the output
# print("Output:", output_data)
#
# predicted_class = np.argmax(output_data)
# print("Predicted class:", predicted_class)
