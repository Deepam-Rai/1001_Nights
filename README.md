
----

<div align="center">
    <img src="https://img.shields.io/badge/Rasa-5A17EE?logo=rasa&logoColor=fff&style=plastic" alt="Rasa Badge" height="22">
    <img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000&style=plastic" alt="Hugging Face Badge" height="22">
    <img src="https://img.shields.io/badge/Ollama-000?logo=ollama&logoColor=fff&style=plastic" alt="Ollama Badge" height="22">
    <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=plastic" alt="Python Badge" height="22">
</div>

# About
This project merges Rasa(Opensource) and LLM together to create a tool that would help users create a story together with AI via browser interface.
   
It uses:
1. RASA opensource as chatbot framework.
2. LLMs services from Huggingface Inference API, Ollama.


# Setup and Running
Setting up:
1. Clone the repo to local.
2. Create a new python environment.
3. Install rasa.
   1. `pip install rasa`

## LLM services
There is a choice to either use locally deployed Ollama service or use Serverless Inference API provided by many models at Huggingface.  

### Huggingface
Getting Huggingface API credentials:
1. Getting text-completion LLM:
   1. Find any text completion model Huggingface that provides Serverless Inference API.
      1. e.g., mistralai/Mistral-7B-v0.1
   2. In the `Deploy` option of the model, `Inference API(Serverless)` will be present.
   3. Click on it and get `API_URL`.
2. Get Huggingface Access Token:
   1. Settings >> Access Tokens >> New Token (Read Access is enough)
Then set following environment variables:
```shell
LLM_SERVICE=HUGGINGFACE
HUGGINGFACE_TOKEN=hf_yourHuggingFaceToken;ReadPermissionIsEnough
HUGGINGFACE_API_URL=https://api-inference.huggingface.co/models/some-model
```


### Ollama
Usual process to install Ollama, pull a model and serve locallu.  
Then set following environment variables:
```shell
LLM_SERVICE=OLLAMA
OLLAMA_MODEL=model-served
OLLAMA_URL=http://localhost:11434/api/generate  # typical url
```


## Training the Rasa chatbot
1. Activate python environment.
2. Train the model: `make train`

## Run the project
1. Activate python environment.
2. Set the Huggingface/Ollama environment variables:
3. Run rasa core server: `make -f Makefile run-server-debug`
4. In another terminal run rasa action server: `rasa run actions --debug`
5. Open the `index.html` file, located inside folder `front_end`, in any browser.

## Usage:
1. Write some line in the center blank page and hit "Continue Story..."
