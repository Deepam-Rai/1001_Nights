
----

<div align="center">
   <img src="https://img.shields.io/badge/Rasa-5A17EE?logo=rasa&logoColor=fff&style=plastic" alt="Rasa Badge" height="22">
   <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=plastic" alt="Docker Badge" height="22">
   <img src="https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000&style=plastic" alt="Hugging Face Badge" height="22">
   <img src="https://img.shields.io/badge/Ollama-000?logo=ollama&logoColor=fff&style=plastic" alt="Ollama Badge" height="22">
   <img src="https://img.shields.io/badge/Prompt%20Engineering-8A2BE2?style=plastic" height="22">
   <img src="https://img.shields.io/badge/Socket.io-010101?logo=socketdotio&logoColor=fff&style=plastic" alt="Socket.io Badge" height="22">
   <img src="https://img.shields.io/badge/Jinja-B41717?logo=jinja&logoColor=fff&style=plastic" alt="Jinja Badge" height="22">
   <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=plastic" alt="Python Badge" height="22">
</div>


----
# About
A story-creation tool where users can take assistance of AI bot via chat interface to build stories!  

Major technologies & techniques used:
1. **RASA opensource:** Chatbot framework.
2. LLMs services:
   1. **Huggingface Inference API:** Serverless Inference API facilitated for some models at Huggingface.
   2. **Ollama:** Locally served.
3. **Docker:** Containerization.
4. **Prompt Engineering:** Guiding bot to understand user and build stories accordingly.


----
# Setup and Running
Setting up:
1. Clone the repo to local.
2. Setup desired LLM service.
   1. Crate `.env` file in root directory during the process.
3. Build docker image.
4. Train rasa model.
5. Run docker containers
   1. Optionally see logs
6. Run ui, interact from browser
7. Start a story or ask AI on right side to get going!

Clone repo:
```shell
git clone https://github.com/Deepam-Rai/1001_Nights.git;
```

## Setup LLM services
There is a choice to either use locally deployed Ollama service or use Serverless Inference API provided by many models at Huggingface.  
To use other service users would need to add their own code to `query_llm()` in `actions/api_llm/utils.py` and set desired environment variables in `.env` file.   

### Ollama
Usual process to install Ollama, pull a model and serve locally:
```shell
# assuming ollama is installed; by default project uses llama3.1 model;
ollama pull llama3.1;  # pull model
ollama run llama3.1;  # serve model
# in the opened terminal interface, can type `/bye` to close interface;
ollama ps;  # check and confirm model serving
```
Configure rasa-action-server to use ollama. Create `.env` file in project root folder and set environment variables:
```shell
LLM_SERVICE=OLLAMA
OLLAMA_MODEL=llama3.1
OLLAMA_URL=http://host.docker.internal:11434/api/generate  # typical url
```

### Huggingface
Getting Huggingface API credentials:
1. Getting text-completion LLM:
   1. Find any text completion model Huggingface that provides Serverless Inference API.
      1. e.g., mistralai/Mistral-7B-v0.1
   2. In the `Deploy` option of the model, `Inference API(Serverless)` will be present.
   3. Click on it and get `API_URL`.
2. Get Huggingface Access Token:
   1. Settings >> Access Tokens >> New Token (Read Access is enough)

Configure rasa-action-server to use Huggingface. Create `.env` file in project-root-folder and set environment variables:
```shell
LLM_SERVICE=HUGGINGFACE
HUGGINGFACE_TOKEN=hf_yourHuggingFaceToken
HUGGINGFACE_API_URL=https://api-inference.huggingface.co/models/some-model
```

## Build docker image
```shell
make build;
```

## Train and Run
```shell
make train;

make run;  # run rasa core-server and action-server

make ui;  # Start python server for UI; visit the shown url;

# optionally see rasa core-server and action-server logs
make core-logs;
make action-logs;

# stop
make stop;
```

## Creating Story with AI:
You can:
- Write some line in the center-story-page and hit _"Continue Story..."_ button.
- Or say something like, _"Lets create a thrilling war story!"_ in the side-chat!
- Or write starting of story in center-story-page and ask bot to add to story in chat!
- You can also ask bot to change any detail, story, whatever in the recent(last two sentences - default settings) part of the story.
