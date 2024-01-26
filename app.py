import streamlit as st
from PIL import Image
from generate_DSL import generate_code
from utils import *
from generate_DSL import *
from generate_HTML import *
import textwrap

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Set page title
st.set_page_config(page_title="Sketch to UI Converter", layout="wide")

# Title
st.title("Sketch to UI Converter")

# Sidebar
st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Load the tokenizer, ViT model, and decoder
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer.add_special_tokens(special_tokens_dict)
vit_model = ViTModel.from_pretrained(
    'google/vit-base-patch16-224').base_model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vit_model.to(device)

decoder = GPT2DecoderWithImageFeatures(input_size=768)
# Update the GPT2 model with the new tokenizer
decoder.gpt.resize_token_embeddings(len(tokenizer))

decoder.load_state_dict(torch.load(
    "best_decoder.pth", map_location=device))
decoder.to(device)

# Main content
while bool(uploaded_file)==True:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
    img_rgb = Image.open(uploaded_file)

    # Perform Conversion
    code_result = generate_code(img_rgb, tokenizer, vit_model, decoder)
    dsl_code = '''{code_result}'''
    # Display extracted text
    st.subheader("Generated DSL Code:")
    st.code(code_result, language='plaintext')

    # Display HTML/CSS code
    st.subheader("Generated HTML/CSS Code:")
    Gemini_HTML_code = generate_HTML(dsl_code)
    HTML_code = Gemini_HTML_code.text
    st.markdown(HTML_code)
    break