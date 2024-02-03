from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from generate_DSL import generate_code
from utils import *
from generate_DSL import *
from generate_HTML import *
import textwrap
from PIL import Image
import io

app = FastAPI()

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

@app.get("/health")
def health():
    response = {
        "status": "ok",
        "message": "Health check passed",
        "data": None
    }
    return response

@app.post("/generate")
async def generate(image: UploadFile = File(...), custom_prompt: str = None):
    image_file = await image.read()
    purpose = custom_prompt
    # Convert to PIL image
    image_file = Image.open(io.BytesIO(image_file))

    code_result = generate_code(image_file, tokenizer, vit_model, decoder)
    gemini_result = generate_HTML(code_result, purpose)

    response = {
        "status": "ok",
        "message": "Generated successfully",
        "input": {
            "custom_prompt": custom_prompt,
            "image": image.filename
        },
        "generated": {
            "dsl": code_result,
            "html": gemini_result.text
        }
    }
    return response