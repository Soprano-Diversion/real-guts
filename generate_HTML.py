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

def generate_HTML(dsl_code):
  model = genai.GenerativeModel('gemini-pro')

  prompt = f'''

You are an expert web developer tasked with converting .GUI code to HTML and CSS. Your role is to analyze the given .GUI code and produce equivalent HTML structure and CSS styling. Follow these steps:

1. Analyze the .GUI code structure and identify the main components and their relationships.

2. Create an HTML structure that represents the layout and elements defined in the .GUI code.

3. Generate CSS code to style the HTML elements, matching the visual properties specified in the .GUI code.

4. Ensure that the resulting HTML/CSS combination accurately represents the original GUI design. Give enough spacing between the elements above and below so that they are clear to see. make sure you add text to all buttons to make them visible. give each div a curved rectangle border so that it's easily identified.

5. If there are any GUI-specific features that don't have a direct HTML/CSS equivalent, provide the closest possible alternative

6. Comment your HTML and CSS code to explain any non-obvious translations or decisions.


Use the following .GUI to HTML/CSS element mapping as a guide:

| .GUI Element    | HTML Element       | CSS Properties                            |
|-----------------|---------------------|-------------------------------------------|
| Window          | <div>               | position: relative; width; height         |
| Button          | <button>            | padding; margin; background-color; border |
| Label           | <label> or <span>   | font-family; font-size; color             |
| TextBox         | <input type="text"> | width; height; border; padding            |
| CheckBox        | <input type="checkbox"> | margin; accent-color                   |
| RadioButton     | <input type="radio">    | margin; accent-color                   |
| ComboBox        | <select>            | width; height; border                     |
| ListBox         | <select multiple>   | width; height; border                     |
| ProgressBar     | <progress>          | width; height; color                      |
| Slider          | <input type="range"> | width; accent-color                      |
| Panel           | <div>               | position: relative; width; height; border |
| TabControl      | <div> with nested <div>s | Use CSS for tabs layout              |
| MenuBar         | <nav> with <ul> and <li> | Use CSS for horizontal layout        |
| ToolBar         | <div> with button elements | Use flexbox for layout             |
| StatusBar       | <footer>            | position: fixed; bottom: 0; width: 100%   |
| Quadruple       | <div>               | display: grid; grid-template-columns: repeat(4, 1fr); |
| Double          | <div>               | display: grid; grid-template-columns: repeat(2, 1fr); |
| Row             | <div>               | display: flex; flex-direction: row;       |

Note: Adapt this mapping as needed based on the specific .GUI code structure and requirements. For layout elements like Quadruple, Double, and Row, consider using CSS Grid or Flexbox for more complex arrangements.

These layout elements can be nested within each other or contain other GUI elements. Adjust the CSS as needed to achieve the desired layout and spacing.

Input: 

{dsl_code}

Output:
1. Converted HTML code
2. Corresponding CSS code

  ''' 

  response = model.generate_content(prompt)
  return response


def generate_response(dsl_code, purpose):
  model = genai.GenerativeModel('gemini-pro')

  generatedHtml = generate_HTML(dsl_code, purpose).text

  react_prompt = f'''Please convert this HTML code to React code.
                    HTML Code:
                    {generatedHtml}
                  '''
  react_response = model.generate_content(react_prompt)

  return {
    "html": generatedHtml,
    "react": react_response.text
  }
  