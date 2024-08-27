# import os
# import django
# import numpy as np
# import tensorflow as tf
# import cv2
# import pathlib
#
# from django.conf import settings
#
# import sys
#
# BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
# sys.path.append(str(BASE_DIR))
#
# # Ensure Django settings are loaded
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midassist.settings')
# django.setup()
#
#
# def load_model():
#     model_path = settings.CheXNet_MODEL_PATH
#     if not os.path.exists(model_path):
#         raise ValueError(f"Could not open '{model_path}'")
#
#     # Load the H5 model using TensorFlow/Keras
#     model = tf.keras.models.load_model(model_path)
#     return model
#
#
# # Preprocess the input image
# def preprocess_image(image_path):
#     # Load the image
#     img = cv2.imread(image_path)
#
#     # Resize the image to the required input size of the model (150x150)
#     img = cv2.resize(img, (150, 150))
#
#     # Normalize the image to have values between 0 and 1
#     img = img.astype(np.float32) / 255.0
#
#     # Add a batch dimension (1, 150, 150, 3)
#     img = np.expand_dims(img, axis=0)
#
#     return img
#
#
# def predict(image_path):
#     model = load_model()
#     input_image = preprocess_image(image_path)
#
#     # Use the model to predict the class
#     output_data = model.predict(input_image)
#     predicted_class = np.argmax(output_data)
#
#     return predicted_class
