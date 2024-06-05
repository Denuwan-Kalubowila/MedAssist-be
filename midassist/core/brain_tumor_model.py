import numpy as np
import tensorflow as tf
import cv2
import pathlib

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="../models/Brain_Tumor1.tflite")

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.allocate_tensors()


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


image_path = "../media/model_images/IMG-20240605-WA0061.jpg"  # Replace with the path to your image
input_image = preprocess_image(image_path)

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], input_image)

# Invoke the interpreter
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

# Print the output
print("Output:", output_data)

# # input details
# print(input_details)
# # output details
# print(output_details)

# for file in pathlib.Path('../media/model_images').iterdir():
#     # read and resize the image
#     img = cv2.imread(r"{}".format(file.resolve()))
#     new_img = cv2.resize(img, (150, 150))
#
#     # Convert the image to float32 and normalize to [0, 1]
#     new_img = new_img.astype(np.float32) / 255.0
#
#     # Add a batch dimension since the model expects input shape: [1, 150, 150, 3]
#     new_img = np.expand_dims(new_img, axis=0)
#
#     # input_details[0]['index'] = the index which accepts the input
#     interpreter.set_tensor(input_details[0]['index'], new_img)
#
#     # run the inference
#     interpreter.invoke()
#
#     # output_details[0]['index'] = the index which provides the output
#     output_data = interpreter.get_tensor(output_details[0]['index'])
#
#     print("For file {}, the output is {}".format(file.stem, output_data))
