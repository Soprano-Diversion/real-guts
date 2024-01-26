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


def generate_HTML(dsl_code):
  model = genai.GenerativeModel('gemini-pro')

  generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
  }

  prompt = f'''Please generate the proper content based on the purpose of the site, style the HTML, the purpose of the site is for reminders and to do. Output the minified HTML and CSS code using the following DSL code!
  {dsl_code}
  ''' 

  response = model.generate_content(prompt)
  return response

