import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import ViTModel, GPT2Tokenizer, AdamW, get_linear_schedule_with_warmup
from PIL import Image

import torch.nn as nn
import torch
from transformers import GPT2LMHeadModel

class GPT2DecoderWithImageFeatures(nn.Module):
    def __init__(self, input_size, gpt_model_name='gpt2'):
        super(GPT2DecoderWithImageFeatures, self).__init__()

        self.gpt = GPT2LMHeadModel.from_pretrained(gpt_model_name)
        self.image_feature_projection = nn.Linear(input_size, self.gpt.config.n_embd)

    def forward(self, input, image_features):
        # Transform the image features to the GPT embedding size
        transformed_image_features = self.image_feature_projection(image_features)

        # Get the input token embeddings
        input_emb = self.gpt.transformer.wte(input)

        # Repeat the transformed image features to match the input sequence length
        repeated_image_features = transformed_image_features.unsqueeze(1).repeat(1, input_emb.size(1), 1)

        # Add the transformed image features to the input token embeddings
        input_emb = input_emb + repeated_image_features

        # Run the GPT model with the updated input
        output = self.gpt(inputs_embeds=input_emb)["logits"]

        return output