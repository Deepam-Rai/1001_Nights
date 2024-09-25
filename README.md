----

<div align="center">
  <img src="https://img.shields.io/badge/Rasa-5A17EE?logo=rasa&logoColor=fff&style=plastic" alt="Rasa Badge" height="22">
   <img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000&style=plastic" alt="Hugging Face Badge" height="22">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=plastic" alt="Python Badge" height="22">
</div>

# About
This is a simple project with aim of using Rasa(Opensource), LLM API together with browser interface. Basically aim is to build a tool to help users create a story together with AI and a chatbot to help guide along the way.  
   
It uses:
1. RASA opensource as chatbot framework.
2. LLMs in form of Huggingface Inference API.


# Setup and Running
Setting up:
1. Clone the repo to local.
2. Create a new python environment.
3. Install rasa.
   1. `pip install rasa`

Getting Huggingface API credentials:
1. Getting text-completion LLM:
   1. Find any text completion model Huggingface that provides Serverless Inference API.
      1. e.g., mistralai/Mistral-7B-v0.1
   2. In the `Deploy` option of the model, `Inference API(Serverless)` will be present.
   3. Click on it and get `API_URL`.
2. Get Huggingface Access Token:
   1. Settings >> Access Tokens >> New Token (Read Access is enough)

Training the Rasa chatbot:
1. Activate python environment.
2. Train the model: `rasa train --domain domain`

Run the project:
1. Activate python environment.
2. Set the Huggingface credentials as environment variables:
   1. `set LLM_API_KEY=your_api_key`
   2. `set LLM_API_URL=api_url` 
3. Run rasa core server: `make -f Makefile run-server-debug`
4. In another terminal run rasa action server: `rasa run actions --debug`
5. Open the `index.html` file, thats inside folder `front_end`, in some browser.

## Usage:
1. Say "hi" in message box.
2. Or directly write some line in the center blank page and hit "Continue Story..."
