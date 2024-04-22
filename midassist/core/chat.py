import vertexai 
from vertexai.language_models import ChatModel
from vertexai import generative_models
import os
from dotenv import load_dotenv

load_dotenv()

vertexai.init(project=os.dotenv('PROJECT'), location=os.dotenv('LOCATION'))
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

def get_response_medassist(request):
    """This method use for get response form vertexai model"""
    response=chat.send_message(request)
    return response


