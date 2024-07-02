# Project README: SketchCraft - The Brain

## Overview

Welcome to SketchCraft - the brain, a powerful LLM that combines image processing and code generation to bridge the gap between design and implementation seamlessly. This project comprises three main modules: `Generate_DSL`, `Generate_HTML`, and `app_fast`. Each module plays a crucial role in transforming visual concepts into functional code.

## Modules:

### 1. Generate_DSL

#### Functionality:
- **generate_code:** Reads an image and converts it into DSL code in the .gui format. This module acts as the first step in translating visual designs into a format suitable for code generation.

### 2. Generate_HTML

#### Functionality:
- Takes DSL code as input and produces HTML and CSS code. This module acts as an intermediary, translating the DSL representation into web-compatible code.

### 3. app_fast

#### Functionality:
- **code_response:** Takes an image and a prompt as input, generating HTML/CSS, React, and more. This module is designed for rapid code generation, making it an ideal choice for fast-paced development.

## How to Use:

### Prerequisites:
- Python 3.9 or higher
- Required dependencies (specified in requirements.txt)

### Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/Soprano-Diversion/real-guts.git
   cd real-guts

2. To use the FAST API to interact:
```bash
  API_KEY=<gemini_key> uvicorn app_fast:app --reload
```
Use Postman or any other API interaction tool to upload the image and get results.
