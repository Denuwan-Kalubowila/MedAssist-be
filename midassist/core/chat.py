"""
  Description:
    This module repesent the chat feature of the MedAssit .
"""
import os
import vertexai
from vertexai.language_models import ChatModel
from vertexai import generative_models
from dotenv import load_dotenv


load_dotenv()

vertexai.init(project=os.getenv('PROJECT'), location=os.getenv('LOCATION'))
chat_model = ChatModel.from_pretrained("chat-bison")
parameters = {
  "candidate_count": 1,
  "max_output_tokens": 1024,
  "temperature": 0.9,
  "top_p": 1
}
safety_settings={
  generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}
chat = chat_model.start_chat(
  context="""Think you are the family doctor. You should able to advice your patients for healthy life.
    You must analyze the patient's requirements well and provide the instructions to do .
     use simple English for understanding instructions to patient."""
)

def get_response_medassist(user_message):
    """
    Gets a response from the Vertex AI chat model.

    Args:
        user_message (str): User's message to the chatbot.

    Returns:
        str: The model's generated response.
    """

    try:
        if not isinstance(user_message, str):
            raise ValueError("user_message must be a string")

        response = chat.send_message(user_message,**parameters)
        return response.text
    except Exception as e:
        print(f"Error getting response: {e}")
        return "An error occurred. Please try again later."