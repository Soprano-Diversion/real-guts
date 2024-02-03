import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import os
import textwrap
import streamlit as st

secret_api_key = os.getenv("API_KEY")
if secret_api_key is None:
    print("Using streamlit API key")
    genai.configure(api_key=st.secrets["api_key"])
else:
    print("Using secret API key")
    genai.configure(api_key=secret_api_key)

generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
  }

def generate_HTML(dsl_code, purpose):
  model = genai.GenerativeModel('gemini-pro')

  prompt = f'''Please generate the proper content based on the purpose of the site, style the HTML using Tailwind CSS framework, the purpose of the site is for online shopping. link the style.css file to html. add lines, spaces and colours wherever it feels necessary. Output the HTML and CSS code!

  DSL Code:
  {dsl_code}
  ''' 

  response = model.generate_content(prompt)
  return response

