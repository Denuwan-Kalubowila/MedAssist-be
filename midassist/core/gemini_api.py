"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import google.generativeai as genai

# Configure the API key
genai.configure(api_key="AIzaSyABwSTHreE8Mzycdt7Yr9g_Ih9zgwx9X28")

# Set up the model with generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

# Define safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction="Now you are the med assist report analysis Ai. You need to act as a very good report analyst. like blood reports, sugar reports, etc. Also in every output you need to mention you are the med assist AI.",
)

# convo = model.start_chat(history=[
# ])
#
# message = extract_text_from_pdf
#
# convo.send_message(message)
# print(convo.last.text)
